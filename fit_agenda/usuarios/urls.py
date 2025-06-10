from django.urls import path
from . import views
from .views import agendar_treino, obter_personais, obter_horarios

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_geral, name='cadastro_geral'),
    path('finalizar-cadastro/cliente/<int:user_id>/', views.finalizar_cadastro_cliente, name='finalizar_cadastro_cliente'),
    path('finalizar-cadastro/personal/<int:trainer_id>/', views.finalizar_cadastro_personal, name='finalizar_cadastro_personal'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('logout/', views.logout_view, name='logout'),
    path('cliente/editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cliente/agendar-treino/', views.agendar_treino, name='agendar_treino'),
    path('cliente/obter-personais/', obter_personais, name='obter_personais'),
    path('cliente/obter-horarios/', obter_horarios, name='obter_horarios'),
    path('cliente/horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('cliente/cancelar-treino/', views.cancelar_treino, name='cancelar_treino'),
    path('cliente/atividades/', views.atividades_cliente, name='atividades_cliente'),
    path('personal/dashboard/', views.dashboard_personal, name='dashboard_personal'),
    path('personal/editar_perfil/', views.editar_perfil_personal, name='editar_perfil_personal'),
    path('personal/editar-dados/', views.editar_dados_personal, name='editar_dados_personal'),
    path('personal/editar-dados-form/', views.editar_dados_form, name='editar_dados_form'),
    path('personal/exercicio-form/<int:treino_id>/', views.exercicio_form_ajax, name='exercicio_form_ajax'),
    path('personal/salvar-exercicio/', views.salvar_exercicio_ajax, name='salvar_exercicio_ajax'),
]
