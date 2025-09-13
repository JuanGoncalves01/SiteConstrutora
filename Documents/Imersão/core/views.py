from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Colaborador, Equipamento, Emprestimo, Itens_Emprestimo
from django.db import transaction
from django.utils import timezone

# View para a página inicial (dashboard)
def home(request):
    colaboradores_count = Colaborador.objects.count()
    epis_count = Equipamento.objects.count()
    emprestimos_ativos_count = Emprestimo.objects.filter(data_devolucao__isnull=True).count()
    return render(request, 'home.html', {
        'colaboradores_count': colaboradores_count,
        'epis_count': epis_count,
        'emprestimos_ativos_count': emprestimos_ativos_count,
    })

# View para verificar o CPF do colaborador e redirecionar para o formulário de empréstimo
def verificar_colaborador(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        try:
            colaborador = Colaborador.objects.get(cpf=cpf)
            return redirect('emprestimo_form_com_cpf', colaborador_id=colaborador.id_colaborador)
        except Colaborador.DoesNotExist:
            messages.error(request, 'Colaborador não encontrado. Por favor, cadastre-o primeiro.')
            return redirect('home')
    return redirect('home')

# View para o formulário de cadastro de colaboradores
def cadastro_colaborador(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        
        if not nome or not cpf:
            messages.error(request, 'Nome e CPF são obrigatórios.')
        else:
            Colaborador.objects.create(nome=nome, cpf=cpf)
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('cadastro_colaborador')
    
    return render(request, 'cadastro_colaborador.html')

# View para o formulário de cadastro de EPI
def cadastro_epi(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        condicao = request.POST.get('condicao')
        situacao = request.POST.get('situacao')
        
        if not nome or not condicao or not situacao:
            messages.error(request, 'Todos os campos são obrigatórios.')
        else:
            Equipamento.objects.create(nome=nome, condicao=condicao, situacao=situacao)
            messages.success(request, 'EPI cadastrado com sucesso!')
            return redirect('cadastro_epi')
    
    return render(request, 'cadastro_epi.html')

# View para listar todos os EPIs
def listar_epis(request):
    epis = Equipamento.objects.all().order_by('nome')
    return render(request, 'listar_epis.html', {'epis': epis})

# View para listar todos os empréstimos ativos
def listar_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(data_devolucao__isnull=True).order_by('data')
    return render(request, 'listar_emprestimos.html', {'emprestimos': emprestimos})

# View para o formulário de empréstimo de EPI
def emprestimo_epi_form(request, colaborador_id=None):
    colaboradores = Colaborador.objects.all()
    epis_disponiveis = Equipamento.objects.filter(situacao=1) # 1 = Disponível
    
    colaborador_selecionado = None
    if colaborador_id:
        colaborador_selecionado = get_object_or_404(Colaborador, id_colaborador=colaborador_id)
    
    return render(request, 'emprestimo.html', {
        'colaboradores': colaboradores, 
        'epis': epis_disponiveis,
        'colaborador_selecionado': colaborador_selecionado
    })

# View para processar o formulário de empréstimo
def confirmar_emprestimo(request):
    if request.method == 'POST':
        colaborador_id = request.POST.get('colaborador')
        epi_id = request.POST.get('epi')
        data_retirada = request.POST.get('data_retirada')
        data_devolucao = request.POST.get('data_devolucao')

        with transaction.atomic():
            try:
                colaborador = Colaborador.objects.get(id_colaborador=colaborador_id)
                epi = Equipamento.objects.get(id_equipamento=epi_id)
            except (Colaborador.DoesNotExist, Equipamento.DoesNotExist):
                messages.error(request, 'Colaborador ou EPI não encontrados.')
                return redirect('emprestimo_form')

            if epi.situacao != 1:
                messages.error(request, 'Este EPI não está disponível no momento.')
                return redirect('emprestimo_form')
            
            if data_devolucao < data_retirada:
                 messages.error(request, 'A data de devolução não pode ser anterior à data de retirada.')
                 return redirect('emprestimo_form')

            novo_emprestimo = Emprestimo.objects.create(
                colaborador=colaborador,
                data=data_retirada,
                data_devolucao=data_devolucao
            )
            
            Itens_Emprestimo.objects.create(
                equipamento=epi,
                emprestimo=novo_emprestimo
            )

            epi.situacao = 2 # 2 = Em Uso
            epi.save()

            messages.success(request, 'Empréstimo realizado com sucesso.')
            return redirect('home')
    
    return redirect('home')

# View para processar a devolução de um EPI
def devolver_emprestimo(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id_emprestimo=emprestimo_id)
    
    # Encontra o item emprestado para atualizar o EPI
    item_emprestimo = Itens_Emprestimo.objects.get(emprestimo=emprestimo)
    epi = item_emprestimo.equipamento
    
    with transaction.atomic():
        # Atualiza a situação do EPI para 'Disponível' (1)
        epi.situacao = 1
        epi.save()

        # Atualiza a data de devolução do empréstimo
        emprestimo.data_devolucao = timezone.now().date()
        emprestimo.save()

    messages.success(request, 'EPI devolvido com sucesso!')
    return redirect('listar_emprestimos')


# View para processar a devolução de um EPI
def devolver_emprestimo(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id_emprestimo=emprestimo_id)
    
    # Encontra o item emprestado para atualizar o EPI
    item_emprestimo = Itens_Emprestimo.objects.get(emprestimo=emprestimo)
    epi = item_emprestimo.equipamento
    
    with transaction.atomic():
        # Atualiza a situação do EPI para 'Disponível' (1)
        epi.situacao = 1
        epi.save()

        # Atualiza a data de devolução do empréstimo
        emprestimo.data_devolucao = timezone.now().date()
        emprestimo.save()

    messages.success(request, 'EPI devolvido com sucesso!')
    return redirect('listar_emprestimos')
 
def listar_epis(request):
    epis = Equipamento.objects.all().order_by('nome')
    return render(request, 'listar_epis.html', {'epis': epis})
