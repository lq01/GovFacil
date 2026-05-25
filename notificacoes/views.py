from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notificacao


@login_required
def lista_notificacoes_view(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user)
    nao_lidas = notificacoes.filter(lida=False).count()

    # Marca todas como lidas ao abrir a página
    notificacoes.filter(lida=False).update(lida=True)

    return render(request, 'notificacoes/lista.html', {
        'notificacoes': notificacoes,
        'nao_lidas': nao_lidas,
    })


@login_required
def marcar_lida_view(request, pk):
    notif = get_object_or_404(Notificacao, pk=pk, usuario=request.user)
    notif.marcar_como_lida()
    return redirect(request.META.get('HTTP_REFERER', 'notificacoes:lista'))


@login_required
def contagem_nao_lidas_view(request):
    count = Notificacao.objects.filter(usuario=request.user, lida=False).count()
    return JsonResponse({'count': count})
