from django.urls import path
from . import views

urlpatterns = [
    # Dashboard / Página Inicial
    path('', views.home, name='home'),

    # Cadastro de Colaboradores
    path('cadastro/colaborador/', views.cadastro_colaborador, name='cadastro_colaborador'),

    # Cadastro de EPI
    path('cadastro/epi/', views.cadastro_epi, name='cadastro_epi'),

    # Listar EPIs
    path('listar/epis/', views.listar_epis, name='listar_epis'),

    # Listar Empréstimos Ativos
    path('listar/emprestimos/', views.listar_emprestimos, name='listar_emprestimos'),

    # Empréstimo rápido / formulário de empréstimo
    path('emprestimo/', views.emprestimo_epi_form, name='emprestimo_epi_form'),

    # Formulário de empréstimo com CPF selecionado
    path('emprestimo/<int:colaborador_id>/', views.emprestimo_epi_form, name='emprestimo_form_com_cpf'),

    # Confirmar empréstimo
    path('emprestimo/confirmar/', views.confirmar_emprestimo, name='confirmar_emprestimo'),

    # Verificar CPF do colaborador
    path('verificar_colaborador/', views.verificar_colaborador, name='verificar_colaborador'),

    # Devolver EPI
    path('devolver/<int:emprestimo_id>/', views.devolver_emprestimo, name='devolver_emprestimo'),

    path('relatorio-colaboradores/', views.relatorio_colaboradores, name='relatorio_colaboradores'),
]
