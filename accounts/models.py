from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Classe base para todos os usuários — aplica Abstração e Encapsulamento."""

    TIPO_CIDADAO = 'cidadao'
    TIPO_SERVIDOR = 'servidor'
    TIPO_CHOICES = [
        (TIPO_CIDADAO, 'Cidadão'),
        (TIPO_SERVIDOR, 'Servidor Público'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_CIDADAO)
    _telefone = models.CharField(max_length=20, blank=True, db_column='telefone')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # Encapsulamento: telefone só é acessado e alterado via property
    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, valor):
        if valor and not all(c.isdigit() or c in '() -+' for c in valor):
            raise ValueError('Telefone inválido.')
        self._telefone = valor or ''

    def get_tipo(self):
        return dict(self.TIPO_CHOICES).get(self.tipo, 'Desconhecido')

    def is_cidadao(self):
        return self.tipo == self.TIPO_CIDADAO

    def is_servidor(self):
        return self.tipo == self.TIPO_SERVIDOR

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name() or self.username


class Cidadao(Usuario):
    """Herança: Cidadao herda de Usuario e adiciona dados e comportamentos do cidadão."""

    _cpf = models.CharField(max_length=14, unique=True, db_column='cpf')
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=300, blank=True)

    # Encapsulamento: CPF só é lido via property, nunca alterado após cadastro
    @property
    def cpf(self):
        return self._cpf

    def solicitar_servico(self, servico, descricao):
        """Cria e abre uma nova solicitação de serviço."""
        from solicitacoes.models import Solicitacao
        sol = Solicitacao(cidadao=self, servico=servico, descricao=descricao)
        sol.abrir()
        return sol

    def consultar_historico(self):
        """Retorna todas as solicitações do cidadão, mais recentes primeiro."""
        return self.solicitacoes.all().order_by('-data_abertura')

    def acompanhar_protocolo(self, numero_protocolo):
        """Busca uma solicitação pelo número de protocolo."""
        from solicitacoes.models import Solicitacao
        return Solicitacao.objects.get(protocolo=numero_protocolo, cidadao=self)

    def receber_notificacoes(self):
        """Retorna notificações não lidas do cidadão."""
        return self.notificacoes.filter(lida=False)

    class Meta:
        verbose_name = 'Cidadão'
        verbose_name_plural = 'Cidadãos'

    def __str__(self):
        return f"{self.get_full_name()} (CPF: {self._cpf})"


class Servidor(Usuario):
    """Herança: Servidor herda de Usuario e adiciona dados e comportamentos do servidor."""

    matricula = models.CharField(max_length=20, unique=True)
    setor = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    def aprovar_solicitacao(self, solicitacao, observacao=''):
        """Aprova uma solicitação pendente."""
        solicitacao.atualizar_status('aprovada', self, observacao or 'Solicitação aprovada.')

    def rejeitar_solicitacao(self, solicitacao, motivo=''):
        """Rejeita uma solicitação com justificativa."""
        solicitacao.atualizar_status('rejeitada', self, motivo or 'Solicitação rejeitada.')

    def atualizar_atendimento(self, solicitacao, novo_status, observacao=''):
        """Atualiza o status de uma solicitação em andamento."""
        solicitacao.atualizar_status(novo_status, self, observacao)

    def listar_solicitacoes_pendentes(self):
        """Lista solicitações abertas ou em análise do setor do servidor."""
        from solicitacoes.models import Solicitacao
        return Solicitacao.objects.filter(
            status__in=['aberta', 'em_analise'],
            setor_responsavel=self.setor,
        ).order_by('data_abertura')

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'

    def __str__(self):
        return f"{self.get_full_name()} — {self.cargo} ({self.setor})"
