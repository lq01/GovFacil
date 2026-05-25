from django.urls import path

from . import views

app_name = 'notificacoes'

urlpatterns = [
    path('', views.lista_notificacoes_view, name='lista'),
    path('<int:pk>/lida/', views.marcar_lida_view, name='marcar_lida'),
    path('api/contagem/', views.contagem_nao_lidas_view, name='contagem'),
]
