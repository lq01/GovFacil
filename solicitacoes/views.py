from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from servicos.models import Servico
from .forms import AtualizarStatusForm, BuscarProtocoloForm, NovaSolicitacaoForm
from .models import Solicitacao


@login_required
def nova_solicitacao_view(request):
    try:
        cidadao = request.user.cidadao
    except Exception:
        messages.error(request, 'Apenas cidadãos podem abrir solicitações.')
        return redirect('core:home')

    servico_inicial = None
    servico_pk = request.GET.get('servico')
    if servico_pk:
        servico_inicial = Servico.objects.filter(pk=servico_pk, ativo=True).first()

    form = NovaSolicitacaoForm(request.POST or None, initial={'servico': servico_inicial})

    if request.method == 'POST' and form.is_valid():
        servico = form.cleaned_data['servico']
        descricao = form.cleaned_data['descricao']
        sol = cidadao.solicitar_servico(servico, descricao)
        messages.success(request, f'Solicitação aberta! Protocolo: {sol.protocolo}')
        return redirect('solicitacoes:detalhe', protocolo=sol.protocolo)

    return render(request, 'solicitacoes/nova.html', {'form': form, 'servico_inicial': servico_inicial})


@login_required
def minhas_solicitacoes_view(request):
    try:
        cidadao = request.user.cidadao
    except Exception:
        return redirect('core:home')

    status_filtro = request.GET.get('status', '')
    solicitacoes = cidadao.consultar_historico()
    if status_filtro:
        solicitacoes = solicitacoes.filter(status=status_filtro)

    return render(request, 'solicitacoes/minhas.html', {
        'solicitacoes': solicitacoes,
        'status_filtro': status_filtro,
        'status_choices': Solicitacao.STATUS_CHOICES,
    })


def detalhe_solicitacao_view(request, protocolo):
    solicitacao = get_object_or_404(Solicitacao, protocolo=protocolo)

    # Cidadão só vê a própria solicitação; servidor vê qualquer uma
    if request.user.is_authenticated and request.user.tipo == 'cidadao':
        try:
            if solicitacao.cidadao != request.user.cidadao:
                messages.error(request, 'Você não tem permissão para ver esta solicitação.')
                return redirect('solicitacoes:minhas')
        except Exception:
            pass

    return render(request, 'solicitacoes/detalhe.html', {'solicitacao': solicitacao})


def buscar_protocolo_view(request):
    form = BuscarProtocoloForm(request.GET or None)
    solicitacao = None
    erro = None

    if form.is_valid():
        protocolo = form.cleaned_data['protocolo'].strip().upper()
        try:
            solicitacao = Solicitacao.objects.get(protocolo=protocolo)
        except Solicitacao.DoesNotExist:
            erro = f'Protocolo "{protocolo}" não encontrado.'

    return render(request, 'solicitacoes/buscar_protocolo.html', {
        'form': form,
        'solicitacao': solicitacao,
        'erro': erro,
    })


@login_required
def painel_servidor_view(request):
    try:
        servidor = request.user.servidor
    except Exception:
        messages.error(request, 'Acesso restrito a servidores.')
        return redirect('core:home')

    status_filtro = request.GET.get('status', '')
    setor_filtro = request.GET.get('setor', '')

    solicitacoes = Solicitacao.objects.select_related('cidadao', 'servico').all()
    if status_filtro:
        solicitacoes = solicitacoes.filter(status=status_filtro)
    if setor_filtro:
        solicitacoes = solicitacoes.filter(setor_responsavel=setor_filtro)

    setores = Solicitacao.objects.values_list('setor_responsavel', flat=True).distinct()

    return render(request, 'solicitacoes/painel_servidor.html', {
        'servidor': servidor,
        'solicitacoes': solicitacoes,
        'status_filtro': status_filtro,
        'setor_filtro': setor_filtro,
        'status_choices': Solicitacao.STATUS_CHOICES,
        'setores': setores,
    })


@login_required
def gerenciar_solicitacao_view(request, protocolo):
    try:
        servidor = request.user.servidor
    except Exception:
        messages.error(request, 'Acesso restrito a servidores.')
        return redirect('core:home')

    solicitacao = get_object_or_404(Solicitacao, protocolo=protocolo)
    form = AtualizarStatusForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        novo_status = form.cleaned_data['status']
        observacao = form.cleaned_data.get('observacao', '')
        servidor.atualizar_atendimento(solicitacao, novo_status, observacao)
        messages.success(request, f'Status atualizado para "{solicitacao.get_status_display()}".')
        return redirect('solicitacoes:painel_servidor')

    return render(request, 'solicitacoes/gerenciar.html', {
        'solicitacao': solicitacao,
        'form': form,
        'servidor': servidor,
    })
