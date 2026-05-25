from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CadastroCidadaoForm, CadastroServidorForm, LoginForm
from .models import Cidadao, Servidor


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('accounts:dashboard')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:home')


def cadastro_cidadao_view(request):
    form = CadastroCidadaoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cidadao = form.save()
        login(request, cidadao)
        messages.success(request, f'Bem-vindo(a), {cidadao.first_name}! Cadastro realizado com sucesso.')
        return redirect('accounts:dashboard_cidadao')
    return render(request, 'accounts/cadastro_cidadao.html', {'form': form})


def cadastro_servidor_view(request):
    form = CadastroServidorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        servidor = form.save()
        login(request, servidor)
        messages.success(request, f'Bem-vindo(a), {servidor.first_name}! Acesso de servidor criado.')
        return redirect('accounts:dashboard_servidor')
    return render(request, 'accounts/cadastro_servidor.html', {'form': form})


@login_required
def dashboard_view(request):
    if request.user.tipo == 'cidadao':
        return redirect('accounts:dashboard_cidadao')
    return redirect('accounts:dashboard_servidor')


@login_required
def dashboard_cidadao_view(request):
    try:
        cidadao = request.user.cidadao
    except Cidadao.DoesNotExist:
        messages.error(request, 'Acesso negado.')
        return redirect('core:home')

    solicitacoes = cidadao.consultar_historico()[:5]
    notificacoes_nao_lidas = cidadao.receber_notificacoes().count()
    total = cidadao.solicitacoes.count()
    concluidas = cidadao.solicitacoes.filter(status='concluida').count()
    em_aberto = cidadao.solicitacoes.filter(
        status__in=['aberta', 'em_analise', 'aprovada', 'em_andamento']
    ).count()

    return render(request, 'accounts/dashboard_cidadao.html', {
        'cidadao': cidadao,
        'solicitacoes': solicitacoes,
        'notificacoes_nao_lidas': notificacoes_nao_lidas,
        'total': total,
        'concluidas': concluidas,
        'em_aberto': em_aberto,
    })


@login_required
def dashboard_servidor_view(request):
    try:
        servidor = request.user.servidor
    except Servidor.DoesNotExist:
        messages.error(request, 'Acesso negado.')
        return redirect('core:home')

    from solicitacoes.models import Solicitacao
    todas = Solicitacao.objects.all()
    pendentes = todas.filter(status__in=['aberta', 'em_analise']).count()
    concluidas = todas.filter(status='concluida').count()
    recentes = todas[:8]

    return render(request, 'accounts/dashboard_servidor.html', {
        'servidor': servidor,
        'pendentes': pendentes,
        'concluidas': concluidas,
        'total': todas.count(),
        'recentes': recentes,
    })
