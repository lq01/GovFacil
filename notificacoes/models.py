from django.conf import settings
from django.db import models


class Notificacao(models.Model):
    """
    Abstração: define o contrato de todas as notificações.
    Polimorfismo: enviar() comporta-se diferente por tipo.
    """

    TIPO_CONFIRMACAO = 'confirmacao'
    TIPO_ATUALIZACAO = 'atualizacao'
    TIPO_LEMBRETE = 'lembrete'

    TIPO_CHOICES = [
        (TIPO_CONFIRMACAO, 'Confirmação'),
        (TIPO_ATUALIZACAO, 'Atualização de Status'),
        (TIPO_LEMBRETE, 'Lembrete'),
    ]

    TIPO_ICONE = {
        TIPO_CONFIRMACAO: 'bi-check-circle-fill text-success',
        TIPO_ATUALIZACAO: 'bi-arrow-repeat text-primary',
        TIPO_LEMBRETE: 'bi-bell-fill text-warning',
    }

    TIPO_COR_FUNDO = {
        TIPO_CONFIRMACAO: 'success',
        TIPO_ATUALIZACAO: 'primary',
        TIPO_LEMBRETE: 'warning',
    }

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_CONFIRMACAO)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificacoes',
    )
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)
    solicitacao = models.ForeignKey(
        'solicitacoes.Solicitacao',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='notificacoes',
    )

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_envio']

    def enviar(self):
        """Polimorfismo: comportamento diferente conforme o tipo da notificação."""
        despachantes = {
            self.TIPO_CONFIRMACAO: self._enviar_confirmacao,
            self.TIPO_ATUALIZACAO: self._enviar_atualizacao,
            self.TIPO_LEMBRETE: self._enviar_lembrete,
        }
        return despachantes.get(self.tipo, lambda: self.mensagem)()

    def _enviar_confirmacao(self):
        return f"[Confirmação] {self.mensagem}"

    def _enviar_atualizacao(self):
        return f"[Atualização] {self.mensagem}"

    def _enviar_lembrete(self):
        return f"[Lembrete] {self.mensagem}"

    def marcar_como_lida(self):
        """Encapsulamento: a lógica de marcar como lida fica dentro da classe."""
        self.lida = True
        self.save(update_fields=['lida'])

    def get_icone(self):
        return self.TIPO_ICONE.get(self.tipo, 'bi-bell')

    def get_cor_fundo(self):
        return self.TIPO_COR_FUNDO.get(self.tipo, 'secondary')

    # ── Fábricas — criam o tipo certo sem expor a lógica interna ──────────

    @classmethod
    def criar_confirmacao(cls, usuario, solicitacao, mensagem):
        notif = cls.objects.create(
            tipo=cls.TIPO_CONFIRMACAO,
            usuario=usuario,
            titulo='Solicitação recebida',
            mensagem=mensagem,
            solicitacao=solicitacao,
        )
        notif.enviar()
        return notif

    @classmethod
    def criar_atualizacao(cls, usuario, solicitacao, mensagem):
        notif = cls.objects.create(
            tipo=cls.TIPO_ATUALIZACAO,
            usuario=usuario,
            titulo='Status atualizado',
            mensagem=mensagem,
            solicitacao=solicitacao,
        )
        notif.enviar()
        return notif

    @classmethod
    def criar_lembrete(cls, usuario, solicitacao, mensagem):
        notif = cls.objects.create(
            tipo=cls.TIPO_LEMBRETE,
            usuario=usuario,
            titulo='Lembrete',
            mensagem=mensagem,
            solicitacao=solicitacao,
        )
        notif.enviar()
        return notif

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.titulo}"


# ── Proxy models — demonstram Polimorfismo via herança ────────────────────

class NotificacaoConfirmacao(Notificacao):
    """Polimorfismo: Confirmacao especializa enviar()."""

    class Meta:
        proxy = True
        verbose_name = 'Notificação de Confirmação'

    def enviar(self):
        return f"✓ Confirmado: {self.mensagem}"


class NotificacaoAtualizacao(Notificacao):
    """Polimorfismo: AtualizacaoStatus especializa enviar()."""

    class Meta:
        proxy = True
        verbose_name = 'Notificação de Atualização'

    def enviar(self):
        return f"↻ Atualização: {self.mensagem}"


class NotificacaoLembrete(Notificacao):
    """Polimorfismo: Lembrete especializa enviar()."""

    class Meta:
        proxy = True
        verbose_name = 'Notificação de Lembrete'

    def enviar(self):
        return f"🔔 Lembrete: {self.mensagem}"
