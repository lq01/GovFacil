from django.contrib import admin

from .models import Notificacao


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'titulo', 'usuario', 'data_envio', 'lida']
    list_filter = ['tipo', 'lida']
    search_fields = ['titulo', 'usuario__username']
    readonly_fields = ['data_envio']
