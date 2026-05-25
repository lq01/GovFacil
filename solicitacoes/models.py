import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Solicitacao(models.Model):
    """Representa uma solicitação de serviço feita por um cidadão."""

    STATUS_ABERTA = 'aberta'
    STATUS_EM_ANALISE = 'em_analise'
    STATUS_APROVADA = 'aprovada'
    STATUS_EM_ANDAMENTO = 'em_andamento'
    STATUS_CONCLUIDA = 'concluida'
    STATUS_REJEITADA = 'rejeitada'

    STATUS_CHOICES = [
        (STATUS_ABERTA, 'Aberta'),
        (STATUS_EM_ANALISE, 'Em Análise'),
        (STATUS_APROVADA, 'Aprovada'),
        (STATUS_EM_ANDAMENTO, 'Em Andamento'),
        (STATUS_CONCLUIDA, 'Concluída'),
        (STATUS_REJEITADA, 'Rejeitada'),
    ]

    STATUS_COR = {
        STATUS_ABERTA: 'primary',
        STATUS_EM_ANALISE: 'warning',
        STATUS_APROVADA: 'info',
        STATUS_EM_ANDAMENTO: 'secondary',
        STATUS_CONCLUIDA: 'success',
        STATUS_REJEITADA: 'danger',
    }

    STATUS_ICONE = {
        STATUS_ABERTA: 'bi-folder2-open',
        STATUS_EM_ANALISE: 'bi-hourglass-split',
        STATUS_APROVADA: 'bi-check-circle',
        STATUS_EM_ANDAMENTO: 'bi-arrow-repeat',
        STATUS_CONCLUIDA: 'bi-check-circle-fill',
        STATUS_REJEITADA: 'bi-x-circle-fill',
    }

    protocolo = models.CharField(max_length=20, unique=True, blank=True)
    cidadao = models.ForeignKey(
        'accounts.Cidadao', on_delete=models.CASCADE, related_name='solicitacoes'
    )
    servico = models.ForeignKey(
        'servicos.Servico', on_delete=models.CASCADE, related_name='solicitacoes'
    )
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ABERTA)
    setor_responsavel = models.CharField(max_length=100, blank=True)
    servidor_responsavel = models.ForeignKey(
        'accounts.Servidor',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='atendimentos',
    )
    observacao = models.TextField(blank=True)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_prazo = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'
        ordering = ['-data_abertura']

    # ── Métodos de negócio ─────────────────────────────────────────────────

    def abrir(self):
        """Abre a solicitação: gera protocolo, define setor e prazo."""
        self.protocolo = self._gerar_protocolo()
        self.setor_responsavel = self.servico.setor_responsavel
        self.data_prazo = self.servico.calcular_prazo()
        self.save()
        self._criar_notificacao_confirmacao()

    def atualizar_status(self, novo_status, servidor=None, observacao=''):
        """Atualiza status, servidor responsável e cria notificação."""
        status_anterior = self.status
        self.status = novo_status
        if servidor:
            self.servidor_responsavel = servidor
        if observacao:
            self.observacao = observacao
        self.save()
        self._criar_notificacao_atualizacao(status_anterior, novo_status)

    def consultar(self):
        return {
            'protocolo': self.protocolo,
            'status': self.get_status_display(),
            'servico': str(self.servico),
            'setor': self.setor_responsavel,
            'data_abertura': self.data_abertura,
            'prazo': self.data_prazo,
        }

    def get_status_cor(self):
        return self.STATUS_COR.get(self.status, 'secondary')

    def get_status_icone(self):
        return self.STATUS_ICONE.get(self.status, 'bi-circle')

    def esta_em_aberto(self):
        return self.status in [self.STATUS_ABERTA, self.STATUS_EM_ANALISE]

    def _gerar_protocolo(self):
        ano = timezone.now().year
        numero = str(uuid.uuid4().int)[:6].zfill(6)
        return f"GF{ano}{numero}"

    def _criar_notificacao_confirmacao(self):
        from notificacoes.models import Notificacao
        Notificacao.criar_confirmacao(
            usuario=self.cidadao,
            solicitacao=self,
            mensagem=(
                f"Sua solicitação foi recebida com sucesso! "
                f"Protocolo: {self.protocolo}. "
                f"Prazo estimado: {self.data_prazo.strftime('%d/%m/%Y') if self.data_prazo else 'a definir'}."
            ),
        )

    def _criar_notificacao_atualizacao(self, status_anterior, status_novo):
        from notificacoes.models import Notificacao
        labels = dict(self.STATUS_CHOICES)
        Notificacao.criar_atualizacao(
            usuario=self.cidadao,
            solicitacao=self,
            mensagem=(
                f"Protocolo {self.protocolo}: status alterado de "
                f"'{labels.get(status_anterior)}' para '{labels.get(status_novo)}'."
            ),
        )

    def __str__(self):
        return f"[{self.protocolo}] {self.servico} — {self.get_status_display()}"


class Historico(models.Model):
    """
    Armazena e organiza o histórico de solicitações de um cidadão.
    Criado automaticamente ao cadastrar o cidadão.
    """

    cidadao = models.OneToOneField(
        'accounts.Cidadao', on_delete=models.CASCADE, related_name='historico'
    )

    class Meta:
        verbose_name = 'Histórico'
        verbose_name_plural = 'Históricos'

    def listar(self):
        return self.cidadao.solicitacoes.all().order_by('-data_abertura')

    def buscar_por_status(self, status):
        return self.cidadao.solicitacoes.filter(status=status)

    def buscar_por_periodo(self, inicio, fim):
        return self.cidadao.solicitacoes.filter(data_abertura__range=[inicio, fim])

    def adicionar_solicitacao(self, solicitacao):
        """A FK em Solicitacao já vincula ao cidadão — método para demonstração POO."""
        pass

    @property
    def total_solicitacoes(self):
        return self.cidadao.solicitacoes.count()

    def __str__(self):
        return f"Histórico de {self.cidadao}"
