from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Colaborador, Equipamento, Emprestimo, Itens_Emprestimo
from django.db import transaction

# View para a página inicial
def home(request):
    return render(request, 'home.html')

# View para o formulário de cadastro de colaboradores
def cadastro_colaborador(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        
        # Validação simples
        if not nome or not cpf:
            messages.error(request, 'Nome e CPF são obrigatórios.')
        else:
            Colaborador.objects.create(nome=nome, cpf=cpf)
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('cadastro_colaborador')
    
    return render(request, 'cadastro_colaborador.html')

# View para o formulário de empréstimo de EPI
def emprestimo_epi_form(request):
    colaboradores = Colaborador.objects.all()
    epis_disponiveis = Equipamento.objects.filter(situacao=1) # 1 = Disponível
    
    return render(request, 'emprestimo.html', {
        'colaboradores': colaboradores, 
        'epis': epis_disponiveis
    })

# View para processar o formulário de empréstimo
def confirmar_emprestimo(request):
    if request.method == 'POST':
        colaborador_id = request.POST.get('colaborador')
        epi_id = request.POST.get('epi')
        data_retirada = request.POST.get('data_retirada')
        data_devolucao = request.POST.get('data_devolucao')

        # Usando transação para garantir atomicidade
        with transaction.atomic():
            try:
                colaborador = Colaborador.objects.get(id_colaborador=colaborador_id)
                epi = Equipamento.objects.get(id_equipamento=epi_id)
            except (Colaborador.DoesNotExist, Equipamento.DoesNotExist):
                messages.error(request, 'Colaborador ou EPI não encontrados.')
                return redirect('emprestimo_form')

            # Requisito: EPI deve estar disponível para empréstimo
            if epi.situacao != 1:
                messages.error(request, 'Este EPI não está disponível no momento.')
                return redirect('emprestimo_form')

            # Requisito: Data de devolução não pode ser anterior à de retirada
            if data_devolucao < data_retirada:
                 messages.error(request, 'A data de devolução não pode ser anterior à data de retirada.')
                 return redirect('emprestimo_form')

            # Cria o registro de Empréstimo
            novo_emprestimo = Emprestimo.objects.create(
                colaborador=colaborador,
                data=data_retirada,
                data_devolucao=data_devolucao
            )
            
            # Cria o registro de Itens_Emprestimo
            Itens_Emprestimo.objects.create(
                equipamento=epi,
                emprestimo=novo_emprestimo
            )

            # Atualiza a situação do EPI para 'Em Uso' (2)
            epi.situacao = 2
            epi.save()

            messages.success(request, 'Empréstimo realizado com sucesso.')
            return redirect('home')
    
    return redirect('home')
