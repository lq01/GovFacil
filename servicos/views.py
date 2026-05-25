from django.shortcuts import get_object_or_404, render

from .models import Servico


def lista_servicos_view(request):
    categoria = request.GET.get('categoria', '')
    servicos = Servico.objects.filter(ativo=True)
    if categoria:
        servicos = servicos.filter(categoria=categoria)

    categorias = Servico.CATEGORIA_CHOICES
    return render(request, 'servicos/lista.html', {
        'servicos': servicos,
        'categorias': categorias,
        'categoria_atual': categoria,
    })


def detalhe_servico_view(request, pk):
    servico = get_object_or_404(Servico, pk=pk, ativo=True)
    prazo = servico.calcular_prazo()
    return render(request, 'servicos/detalhe.html', {
        'servico': servico,
        'prazo': prazo,
        'resultado_processar': servico.processar(),
    })
