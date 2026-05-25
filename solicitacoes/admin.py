from django.contrib import admin

from .models import Historico, Solicitacao


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ['protocolo', 'cidadao', 'servico', 'status', 'setor_responsavel', 'data_abertura']
    list_filter = ['status', 'setor_responsavel']
    search_fields = ['protocolo', 'cidadao__first_name', 'cidadao__last_name']
    readonly_fields = ['protocolo', 'data_abertura', 'data_atualizacao']


@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ['cidadao', 'total_solicitacoes']
