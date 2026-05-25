from django.shortcuts import render

from servicos.models import Servico


def home_view(request):
    servicos_destaque = Servico.objects.filter(ativo=True)[:6]

    passos = [
        ('1', 'bi-person-plus', 'Cadastre-se', 'Crie sua conta com CPF em menos de 2 minutos.'),
        ('2', 'bi-card-checklist', 'Escolha o serviço', 'Selecione o serviço que precisa e preencha os dados.'),
        ('3', 'bi-bell-fill', 'Acompanhe', 'Receba atualizações e acompanhe pelo número de protocolo.'),
    ]

    vantagens = [
        ('bi-clock-history', 'Sem filas', 'Solicite serviços 24h sem sair de casa.'),
        ('bi-shield-check', 'Seguro', 'Dados protegidos com autenticação segura.'),
        ('bi-graph-up', 'Transparente', 'Acompanhe cada etapa do seu atendimento.'),
        ('bi-phone', 'Acessível', 'Funciona em qualquer dispositivo.'),
    ]

    return render(request, 'core/home.html', {
        'servicos_destaque': servicos_destaque,
        'passos': passos,
        'vantagens': vantagens,
    })
