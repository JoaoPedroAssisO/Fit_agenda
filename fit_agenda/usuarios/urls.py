from django.urls import path
from . import views
from .views import finalizar_cadastro_cliente, finalizar_cadastro_personal

urlpatterns = [
    path('login/', views.login_view, name='login'),
   path('cadastro/', views.cadastro_geral, name='cadastro_geral'),
   path('finalizar-cadastro/cliente/<int:user_id>/', views.finalizar_cadastro_cliente, name='finalizar_cadastro_cliente'),
   path('finalizar-cadastro/personal/<int:trainer_id>/', views.finalizar_cadastro_personal, name='finalizar_cadastro_personal'),

]
