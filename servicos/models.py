from datetime import timedelta

from django.db import models
from django.utils import timezone


class Servico(models.Model):
    """
    Abstração: define o contrato de todos os serviços públicos.
    Subclasses especializam processar() e calcular_prazo() — Polimorfismo.
    """

    CATEGORIA_EMISSAO = 'emissao'
    CATEGORIA_AGENDAMENTO = 'agendamento'
    CATEGORIA_PROTOCOLO = 'protocolo'
    CATEGORIA_SEGUNDA_VIA = 'segunda_via'

    CATEGORIA_CHOICES = [
        (CATEGORIA_EMISSAO, 'Emissão de Documento'),
        (CATEGORIA_AGENDAMENTO, 'Agendamento'),
        (CATEGORIA_PROTOCOLO, 'Protocolo'),
        (CATEGORIA_SEGUNDA_VIA, 'Segunda Via'),
    ]

    CATEGORIA_ICONE = {
        CATEGORIA_EMISSAO: 'bi-file-earmark-text',
        CATEGORIA_AGENDAMENTO: 'bi-calendar-check',
        CATEGORIA_PROTOCOLO: 'bi-journal-text',
        CATEGORIA_SEGUNDA_VIA: 'bi-files',
    }

    CATEGORIA_COR = {
        CATEGORIA_EMISSAO: 'primary',
        CATEGORIA_AGENDAMENTO: 'success',
        CATEGORIA_PROTOCOLO: 'warning',
        CATEGORIA_SEGUNDA_VIA: 'info',
    }

    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    prazo_dias = models.IntegerField(default=5)
    setor_responsavel = models.CharField(max_length=100, default='Atendimento Geral')
    ativo = models.BooleanField(default=True)

    def processar(self):
        """Método base — subclasses devem especializar (Polimorfismo)."""
        return f"Processando serviço: {self.nome}"

    def calcular_prazo(self):
        """Calcula a data limite de atendimento."""
        return timezone.now() + timedelta(days=self.prazo_dias)

    def consultar(self):
        return {
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria': self.get_categoria_display(),
            'prazo_dias': self.prazo_dias,
            'setor': self.setor_responsavel,
        }

    def get_icone(self):
        return self.CATEGORIA_ICONE.get(self.categoria, 'bi-gear')

    def get_cor(self):
        return self.CATEGORIA_COR.get(self.categoria, 'secondary')

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['categoria', 'nome']

    def __str__(self):
        return self.nome


# ── Subclasses — demonstram Herança e Polimorfismo ──────────────────────────

class EmissaoDocumento(Servico):
    """Herança + Polimorfismo: especializa processar() e calcular_prazo()."""

    tipo_documento = models.CharField(max_length=100)
    requer_autenticacao = models.BooleanField(default=False)

    def processar(self):
        auth = ' (requer autenticação)' if self.requer_autenticacao else ''
        return f"Emitindo {self.tipo_documento}{auth}."

    def calcular_prazo(self):
        extra = 2 if self.requer_autenticacao else 0
        return timezone.now() + timedelta(days=self.prazo_dias + extra)

    class Meta:
        verbose_name = 'Emissão de Documento'
        verbose_name_plural = 'Emissões de Documento'


class Agendamento(Servico):
    """Herança + Polimorfismo: prazo fixo de 1 dia (confirmação rápida)."""

    local_atendimento = models.CharField(max_length=200)
    horarios_disponiveis = models.JSONField(default=list, blank=True)

    def processar(self):
        return f"Agendamento confirmado em: {self.local_atendimento}."

    def calcular_prazo(self):
        return timezone.now() + timedelta(days=1)

    def listar_horarios(self):
        return self.horarios_disponiveis

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'


class Protocolo(Servico):
    """Herança + Polimorfismo: registro formal de solicitações e denúncias."""

    orgao_destino = models.CharField(max_length=200)
    permite_anonimo = models.BooleanField(default=False)

    def processar(self):
        return f"Protocolo registrado e encaminhado para: {self.orgao_destino}."

    def calcular_prazo(self):
        return timezone.now() + timedelta(days=self.prazo_dias)

    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'


class SegundaVia(Servico):
    """Herança + Polimorfismo: segunda via de documentos com prazo estendido."""

    documento_original = models.CharField(max_length=100)
    taxa_emissao = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def processar(self):
        taxa = f"Taxa: R$ {self.taxa_emissao:.2f}" if self.taxa_emissao > 0 else "Gratuita"
        return f"Segunda via de {self.documento_original}. {taxa}."

    def calcular_prazo(self):
        return timezone.now() + timedelta(days=self.prazo_dias + 1)

    class Meta:
        verbose_name = 'Segunda Via'
        verbose_name_plural = 'Segundas Vias'
