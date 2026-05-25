from django.urls import path

from . import views

app_name = 'servicos'

urlpatterns = [
    path('', views.lista_servicos_view, name='lista'),
    path('<int:pk>/', views.detalhe_servico_view, name='detalhe'),
]
