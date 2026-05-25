from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Cidadao, Servidor, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'email', 'tipo', 'data_cadastro']
    list_filter = ['tipo', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('GovFácil', {'fields': ('tipo', '_telefone')}),
    )


@admin.register(Cidadao)
class CidadaoAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', '_cpf', 'email', 'endereco', 'data_cadastro']
    search_fields = ['first_name', 'last_name', '_cpf', 'email']


@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'matricula', 'setor', 'cargo', 'email']
    list_filter = ['setor']
    search_fields = ['first_name', 'last_name', 'matricula']
