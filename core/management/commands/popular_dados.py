from django.core.management.base import BaseCommand

from accounts.models import Cidadao, Servidor, Usuario
from servicos.models import Agendamento, EmissaoDocumento, Protocolo, SegundaVia, Servico
from solicitacoes.models import Historico


class Command(BaseCommand):
    help = 'Popula o banco com dados de demonstração'

    def handle(self, *args, **options):
        self.stdout.write('Populando dados iniciais...')

        # ── Serviços ──────────────────────────────────────────────────────
        servicos_criados = 0

        if not Servico.objects.filter(nome='Certidão de Nascimento').exists():
            EmissaoDocumento.objects.create(
                nome='Certidão de Nascimento',
                descricao='Emissão de certidão de nascimento para uso em órgãos públicos.',
                categoria='emissao',
                prazo_dias=5,
                setor_responsavel='Documentação',
                tipo_documento='Certidão de Nascimento',
                requer_autenticacao=False,
            )
            servicos_criados += 1

        if not Servico.objects.filter(nome='Carteira de Identidade (RG)').exists():
            EmissaoDocumento.objects.create(
                nome='Carteira de Identidade (RG)',
                descricao='Emissão da carteira de identidade para cidadãos acima de 16 anos.',
                categoria='emissao',
                prazo_dias=10,
                setor_responsavel='Documentação',
                tipo_documento='Carteira de Identidade',
                requer_autenticacao=True,
            )
            servicos_criados += 1

        if not Servico.objects.filter(nome='Agendamento Médico — UBS').exists():
            Agendamento.objects.create(
                nome='Agendamento Médico — UBS',
                descricao='Agende uma consulta médica na Unidade Básica de Saúde mais próxima.',
                categoria='agendamento',
                prazo_dias=1,
                setor_responsavel='Saúde',
                local_atendimento='UBS Central — Rua das Flores, 100',
                horarios_disponiveis=['08:00', '09:00', '10:00', '14:00', '15:00', '16:00'],
            )
            servicos_criados += 1

        if not Servico.objects.filter(nome='Agendamento de Vistoria').exists():
            Agendamento.objects.create(
                nome='Agendamento de Vistoria',
                descricao='Solicite vistoria técnica para imóveis e estabelecimentos.',
                categoria='agendamento',
                prazo_dias=3,
                setor_responsavel='Fiscalização',
                local_atendimento='Secretaria de Obras — Av. Brasil, 500',
                horarios_disponiveis=['09:00', '11:00', '14:00', '16:00'],
            )
            servicos_criados += 1

        if not Servico.objects.filter(nome='Protocolo de Denúncia').exists():
            Protocolo.objects.create(
                nome='Protocolo de Denúncia',
                descricao='Registre denúncias sobre irregularidades nos serviços públicos.',
                categoria='protocolo',
                prazo_dias=15,
                setor_responsavel='Ouvidoria',
                orgao_destino='Ouvidoria Municipal',
                permite_anonimo=True,
            )
            servicos_criados += 1

        if not Servico.objects.filter(nome='Protocolo de Requerimento').exists():
            Protocolo.objects.create(
                nome='Protocolo de Requerimento',
                descricao='Protocole requerimentos e pedidos formais à administração pública.',
                categoria='protocolo',
                prazo_dias=30,
                setor_responsavel='Atendimento Geral',
                orgao_destino='Secretaria Geral',
                permite_anonimo=False,
            )
            servicos_criados += 1

        if not Servico.objects.filter(nome='Segunda Via do RG').exists():
            SegundaVia.objects.create(
                nome='Segunda Via do RG',
                descricao='Solicite a segunda via da carteira de identidade em caso de perda ou roubo.',
                categoria='segunda_via',
                prazo_dias=7,
                setor_responsavel='Documentação',
                documento_original='Carteira de Identidade (RG)',
                taxa_emissao=0,
            )
            servicos_criados += 1

        if not Servico.objects.filter(nome='Segunda Via do Alvará').exists():
            SegundaVia.objects.create(
                nome='Segunda Via do Alvará',
                descricao='Segunda via do alvará de funcionamento para estabelecimentos comerciais.',
                categoria='segunda_via',
                prazo_dias=10,
                setor_responsavel='Tributação',
                documento_original='Alvará de Funcionamento',
                taxa_emissao=45.00,
            )
            servicos_criados += 1

        self.stdout.write(f'  {servicos_criados} serviços criados.')

        # ── Servidor de demonstração ──────────────────────────────────────
        if not Servidor.objects.filter(matricula='SRV001').exists():
            srv = Servidor(
                username='servidor',
                email='servidor@govfacil.gov.br',
                first_name='Carlos',
                last_name='Oliveira',
                tipo=Usuario.TIPO_SERVIDOR,
                matricula='SRV001',
                setor='Documentação',
                cargo='Atendente',
            )
            srv.set_password('senha123')
            srv.save()
            self.stdout.write('  Servidor demo criado: usuário=servidor / senha=senha123')

        # ── Cidadão de demonstração ───────────────────────────────────────
        if not Cidadao.objects.filter(_cpf='12345678901').exists():
            cid = Cidadao(
                username='cidadao',
                email='cidadao@email.com',
                first_name='Maria',
                last_name='Silva',
                tipo=Usuario.TIPO_CIDADAO,
                _cpf='12345678901',
                endereco='Rua das Acácias, 42',
            )
            cid.set_password('senha123')
            cid.save()
            Historico.objects.get_or_create(cidadao=cid)
            self.stdout.write('  Cidadão demo criado: usuário=cidadao / senha=senha123')

        self.stdout.write(self.style.SUCCESS('\nDados populados com sucesso!'))
        self.stdout.write('Acesse: http://127.0.0.1:8000/')
        self.stdout.write('Admin:  http://127.0.0.1:8000/admin/')
