from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro_colaborador/', views.cadastro_colaborador, name='cadastro_colaborador'),
    path('emprestimo/', views.emprestimo_epi_form, name='emprestimo_form'),
    path('emprestimo/confirmar/', views.confirmar_emprestimo, name='confirmar_emprestimo'),
]
