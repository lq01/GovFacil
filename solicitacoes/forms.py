from django import forms

from servicos.models import Servico
from .models import Solicitacao


class NovaSolicitacaoForm(forms.Form):
    servico = forms.ModelChoiceField(
        queryset=Servico.objects.filter(ativo=True),
        label='Serviço',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Selecione um serviço...',
    )
    descricao = forms.CharField(
        label='Descreva sua solicitação',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Informe os detalhes necessários para atender sua solicitação...',
        }),
    )


class AtualizarStatusForm(forms.Form):
    STATUS_CHOICES = [
        ('em_analise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('rejeitada', 'Rejeitada'),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label='Novo Status',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    observacao = forms.CharField(
        label='Observação',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Informe detalhes sobre a atualização (opcional)...',
        }),
    )


class BuscarProtocoloForm(forms.Form):
    protocolo = forms.CharField(
        label='Número do protocolo',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ex: GF2025123456',
        }),
    )
