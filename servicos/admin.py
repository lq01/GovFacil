from django.contrib import admin

from .models import Agendamento, EmissaoDocumento, Protocolo, SegundaVia, Servico


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'prazo_dias', 'setor_responsavel', 'ativo']
    list_filter = ['categoria', 'ativo']
    search_fields = ['nome']
    list_editable = ['ativo']


@admin.register(EmissaoDocumento)
class EmissaoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_documento', 'requer_autenticacao', 'prazo_dias']


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'local_atendimento', 'prazo_dias']


@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'orgao_destino', 'permite_anonimo']


@admin.register(SegundaVia)
class SegundaViaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'documento_original', 'taxa_emissao']
