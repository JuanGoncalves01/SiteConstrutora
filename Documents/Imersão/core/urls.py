from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('verificar_colaborador/', views.verificar_colaborador, name='verificar_colaborador'),
    path('cadastro_colaborador/', views.cadastro_colaborador, name='cadastro_colaborador'),
    path('cadastro_epi/', views.cadastro_epi, name='cadastro_epi'),
    path('listar_epis/', views.listar_epis, name='listar_epis'),
    path('listar_emprestimos/', views.listar_emprestimos, name='listar_emprestimos'),
    path('emprestimo/', views.emprestimo_epi_form, name='emprestimo_form'),
    path('emprestimo/<int:colaborador_id>/', views.emprestimo_epi_form, name='emprestimo_form_com_cpf'),
    path('emprestimo/confirmar/', views.confirmar_emprestimo, name='confirmar_emprestimo'),
    path('devolver/<int:emprestimo_id>/', views.devolver_emprestimo, name='devolver_emprestimo'),
]