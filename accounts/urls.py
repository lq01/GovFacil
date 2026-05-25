from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/cidadao/', views.cadastro_cidadao_view, name='cadastro_cidadao'),
    path('cadastro/servidor/', views.cadastro_servidor_view, name='cadastro_servidor'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/cidadao/', views.dashboard_cidadao_view, name='dashboard_cidadao'),
    path('dashboard/servidor/', views.dashboard_servidor_view, name='dashboard_servidor'),
]
