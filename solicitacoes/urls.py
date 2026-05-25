from django.urls import path

from . import views

app_name = 'solicitacoes'

urlpatterns = [
    path('nova/', views.nova_solicitacao_view, name='nova'),
    path('minhas/', views.minhas_solicitacoes_view, name='minhas'),
    path('protocolo/<str:protocolo>/', views.detalhe_solicitacao_view, name='detalhe'),
    path('buscar/', views.buscar_protocolo_view, name='buscar'),
    path('painel/', views.painel_servidor_view, name='painel_servidor'),
    path('gerenciar/<str:protocolo>/', views.gerenciar_solicitacao_view, name='gerenciar'),
]
