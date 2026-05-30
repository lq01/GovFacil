# GovFácil — Documentação do Projeto
**Disciplina:** Programação Orientada a Objetos  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Tema:** Serviços Públicos Digitais

---

## 1. Nome do Sistema

**GovFácil** — Plataforma Digital de Serviços Públicos

O nome une "Gov" (governo) com "Fácil", transmitindo a proposta central do sistema: tornar o acesso aos serviços públicos simples, rápido e acessível para qualquer cidadão.

---

## 2. Objetivo do Sistema

### Problema que o sistema resolve

O cidadão brasileiro enfrenta diariamente dificuldades para acessar serviços públicos: longas filas presenciais, processos burocráticos sem transparência, falta de comunicação sobre o andamento de solicitações e dificuldade para saber qual órgão procurar para cada tipo de serviço.

### O que o GovFácil resolve

O GovFácil centraliza os principais serviços públicos em uma única plataforma digital, permitindo que o cidadão solicite serviços, acompanhe protocolos e receba atualizações sem sair de casa. Para os servidores públicos, o sistema oferece um painel de gestão para organizar, aprovar e responder às solicitações com eficiência.

### Quem utiliza o sistema

| Perfil | Descrição |
|---|---|
| **Cidadão** | Pessoa física que solicita serviços públicos |
| **Servidor** | Funcionário público que gerencia e responde às solicitações |

### Finalidade principal

Reduzir burocracia, eliminar filas presenciais e garantir transparência no atendimento ao cidadão por meio de uma plataforma web acessível e organizada.

---

## 3. Modelagem das Classes

O sistema é composto por **8 classes principais**, organizadas em hierarquias de herança e responsabilidades bem definidas.

### Diagrama de Hierarquia

```
Usuario  (classe base)
├── Cidadao
└── Servidor

Servico  (classe abstrata)
├── EmissaoDocumento
├── Agendamento
├── Protocolo
└── SegundaVia

Solicitacao
Notificacao  (classe abstrata)
├── Confirmacao
├── AtualizacaoStatus
└── Lembrete

Historico
```

### Descrição de cada classe

| Classe | Tipo | Descrição |
|---|---|---|
| `Usuario` | Base (herança) | Classe pai de todos os usuários do sistema |
| `Cidadao` | Filha de Usuario | Representa o cidadão que solicita serviços |
| `Servidor` | Filha de Usuario | Representa o servidor público que gerencia atendimentos |
| `Servico` | Abstrata | Define o contrato de todos os tipos de serviço |
| `EmissaoDocumento` | Filha de Servico | Serviço de emissão de documentos oficiais |
| `Agendamento` | Filha de Servico | Serviço de agendamento de atendimento presencial |
| `Protocolo` | Filha de Servico | Registro e acompanhamento de protocolos |
| `SegundaVia` | Filha de Servico | Solicitação de segunda via de documentos |
| `Solicitacao` | Independente | Representa uma solicitação feita por um cidadão |
| `Notificacao` | Abstrata | Classe base para todos os tipos de notificação |
| `Confirmacao` | Filha de Notificacao | Notificação de confirmação de abertura |
| `AtualizacaoStatus` | Filha de Notificacao | Notificação de mudança de status |
| `Lembrete` | Filha de Notificacao | Notificação de lembrete de agendamento |
| `Historico` | Independente | Armazena o histórico de solicitações do cidadão |

---

## 4. Atributos das Classes

### Usuario (classe base)
| Atributo | Tipo | Descrição |
|---|---|---|
| `nome` | String | Nome completo do usuário |
| `email` | String | Endereço de e-mail (login) |
| `senha` | String | Senha de acesso (armazenada com criptografia) |
| `telefone` | String | Número de contato |
| `dataCadastro` | DateTime | Data e hora do cadastro |
| `ativo` | Boolean | Indica se a conta está ativa |

### Cidadao (herda de Usuario)
| Atributo | Tipo | Descrição |
|---|---|---|
| `cpf` | String | CPF do cidadão (identificador único) |
| `dataNascimento` | Date | Data de nascimento |
| `endereco` | String | Endereço residencial |

### Servidor (herda de Usuario)
| Atributo | Tipo | Descrição |
|---|---|---|
| `matricula` | String | Matrícula funcional (identificador único) |
| `setor` | String | Setor onde atua (ex: Documentação, Saúde) |
| `cargo` | String | Cargo ocupado |

### Servico (classe abstrata)
| Atributo | Tipo | Descrição |
|---|---|---|
| `nome` | String | Nome do serviço |
| `descricao` | String | Descrição detalhada |
| `categoria` | String | Categoria do serviço |
| `prazoDias` | Integer | Prazo de atendimento em dias |
| `ativo` | Boolean | Se o serviço está disponível |

### EmissaoDocumento (herda de Servico)
| Atributo | Tipo | Descrição |
|---|---|---|
| `tipoDocumento` | String | Tipo do documento a ser emitido |
| `requerAutenticacao` | Boolean | Se precisa de autenticação em cartório |

### Agendamento (herda de Servico)
| Atributo | Tipo | Descrição |
|---|---|---|
| `localAtendimento` | String | Endereço do local de atendimento |
| `horariosDisponiveis` | Lista | Lista de horários disponíveis |

### Solicitacao
| Atributo | Tipo | Descrição |
|---|---|---|
| `protocolo` | String | Número único de protocolo gerado automaticamente |
| `status` | String | Status atual (Aberta / Em Análise / Aprovada / Concluída / Rejeitada) |
| `descricao` | String | Descrição do que o cidadão solicita |
| `dataAbertura` | DateTime | Data e hora de criação da solicitação |
| `dataAtualizacao` | DateTime | Data e hora da última atualização |
| `setorResponsavel` | String | Setor responsável pelo atendimento |
| `observacao` | String | Observações do servidor sobre o atendimento |

### Notificacao (classe abstrata)
| Atributo | Tipo | Descrição |
|---|---|---|
| `titulo` | String | Título da notificação |
| `mensagem` | String | Conteúdo da notificação |
| `dataEnvio` | DateTime | Data e hora do envio |
| `lida` | Boolean | Se o usuário já visualizou |

### Historico
| Atributo | Tipo | Descrição |
|---|---|---|
| `cidadao` | Cidadao | Referência ao cidadão dono do histórico |
| `solicitacoes` | Lista | Lista de todas as solicitações realizadas |
| `totalSolicitacoes` | Integer | Contador total de solicitações |

---

## 5. Métodos das Classes

### Usuario
| Método | Descrição |
|---|---|
| `cadastrar()` | Registra um novo usuário no sistema |
| `autenticar(email, senha)` | Valida o login do usuário |
| `atualizar()` | Atualiza os dados do perfil |
| `desativar()` | Desativa a conta do usuário |
| `getTipo()` | Retorna o tipo de usuário (cidadão ou servidor) |

### Cidadao
| Método | Descrição |
|---|---|
| `solicitarServico(servico, descricao)` | Abre uma nova solicitação de serviço |
| `acompanharProtocolo(numeroProtocolo)` | Consulta o status de uma solicitação pelo protocolo |
| `consultarHistorico()` | Retorna todas as solicitações realizadas |
| `receberNotificacao()` | Verifica e lista notificações não lidas |

### Servidor
| Método | Descrição |
|---|---|
| `aprovarSolicitacao(solicitacao)` | Aprova uma solicitação pendente |
| `rejeitarSolicitacao(solicitacao, motivo)` | Rejeita uma solicitação com justificativa |
| `atualizarAtendimento(solicitacao, status, obs)` | Atualiza o status de uma solicitação em andamento |
| `listarSolicitacoesPendentes()` | Lista todas as solicitações aguardando análise do setor |

### Servico (abstrata)
| Método | Descrição |
|---|---|
| `processar()` | **Abstrato** — cada subtipo implementa como o serviço é processado |
| `calcularPrazo()` | **Abstrato** — cada subtipo calcula seu próprio prazo de atendimento |
| `consultar()` | Retorna as informações do serviço |

### EmissaoDocumento (sobrescreve Servico)
| Método | Descrição |
|---|---|
| `processar()` | Processa a emissão do documento solicitado |
| `calcularPrazo()` | Calcula prazo somando dias extras se exigir autenticação |

### Agendamento (sobrescreve Servico)
| Método | Descrição |
|---|---|
| `processar()` | Confirma e registra o agendamento no horário escolhido |
| `calcularPrazo()` | Retorna prazo fixo de 1 dia (confirmação imediata) |
| `listarHorarios()` | Retorna horários disponíveis para escolha |

### Solicitacao
| Método | Descrição |
|---|---|
| `abrir()` | Cria a solicitação e gera o número de protocolo |
| `atualizarStatus(novoStatus, servidor, obs)` | Atualiza o status e registra o servidor responsável |
| `consultar()` | Retorna todos os dados da solicitação |
| `gerarProtocolo()` | Gera um número de protocolo único automaticamente |

### Notificacao (abstrata)
| Método | Descrição |
|---|---|
| `enviar()` | **Abstrato** — cada subtipo define como a notificação é enviada |
| `marcarComoLida()` | Marca a notificação como visualizada |

### Confirmacao / AtualizacaoStatus / Lembrete (sobrescrevem Notificacao)
| Método | Descrição |
|---|---|
| `enviar()` | Cada subclasse envia a notificação com mensagem específica ao contexto |

### Historico
| Método | Descrição |
|---|---|
| `adicionarSolicitacao(solicitacao)` | Inclui uma nova solicitação no histórico |
| `listar()` | Retorna todas as solicitações do cidadão |
| `buscarPorStatus(status)` | Filtra solicitações por status |
| `buscarPorPeriodo(inicio, fim)` | Filtra solicitações por data |

---

## 6. Aplicação dos 4 Pilares da POO

### Encapsulamento

> *"Proteger os dados internos e expor apenas o necessário."*

No GovFácil, o encapsulamento é aplicado em toda a camada de modelos:

- O atributo `_senha` do `Usuario` é privado e nunca acessado diretamente — o acesso ocorre apenas pelo método `autenticar()`, que realiza a verificação com criptografia internamente.
- O atributo `_cpf` do `Cidadao` é privado e exposto apenas via propriedade, impedindo que seja alterado externamente sem validação.
- O atributo `_status` da `Solicitacao` só pode ser alterado pelo método `atualizarStatus()`, que valida se a transição de status é permitida antes de executar a mudança.
- Os detalhes de como `gerarProtocolo()` cria o número único são internos à classe `Solicitacao` — quem chama o método não precisa saber como funciona.

**Benefício:** Qualquer regra de negócio (como validar CPF ou verificar senha) fica concentrada dentro da classe, não espalhada pelo sistema.

---

### Herança

> *"Reutilizar comportamentos comuns e especializar onde necessário."*

O GovFácil possui duas hierarquias principais de herança:

**Hierarquia de Usuários:**
```
Usuario
├── Cidadao   → herda nome, email, senha, telefone, dataCadastro
│              → adiciona: cpf, dataNascimento, endereco
│              → adiciona: solicitarServico(), consultarHistorico()
└── Servidor  → herda nome, email, senha, telefone, dataCadastro
               → adiciona: matricula, setor, cargo
               → adiciona: aprovarSolicitacao(), rejeitarSolicitacao()
```

**Hierarquia de Serviços:**
```
Servico (abstrata)
├── EmissaoDocumento → herda nome, descricao, prazo → especializa processar() e calcularPrazo()
├── Agendamento      → herda nome, descricao, prazo → especializa processar() e calcularPrazo()
├── Protocolo        → herda nome, descricao, prazo → especializa processar() e calcularPrazo()
└── SegundaVia       → herda nome, descricao, prazo → especializa processar() e calcularPrazo()
```

**Benefício:** O código de `cadastrar()`, `autenticar()` e `atualizar()` é escrito uma única vez em `Usuario` e funciona para `Cidadao` e `Servidor` sem repetição.

---

### Polimorfismo

> *"O mesmo método se comporta de formas diferentes dependendo do objeto."*

O polimorfismo aparece em dois pontos centrais do sistema:

**1. Método `processar()` em Servico:**

```
EmissaoDocumento.processar()  → "Emitindo certidão de nascimento..."
Agendamento.processar()       → "Confirmando horário às 14h no Paço Municipal..."
Protocolo.processar()         → "Registrando protocolo de denúncia..."
SegundaVia.processar()        → "Solicitando segunda via do título de eleitor..."
```

Todos são chamados da mesma forma: `servico.processar()`. O sistema não precisa saber qual tipo de serviço é — ele simplesmente chama o método e cada classe sabe o que fazer.

**2. Método `enviar()` em Notificacao:**

```
Confirmacao.enviar()        → "Sua solicitação foi recebida. Protocolo: #00123"
AtualizacaoStatus.enviar()  → "Sua solicitação foi aprovada e está em andamento."
Lembrete.enviar()           → "Lembrete: seu agendamento é amanhã às 10h."
```

**Benefício:** O sistema pode iterar sobre uma lista de notificações e chamar `enviar()` em cada uma sem precisar verificar o tipo — cada objeto sabe como se comportar.

---

### Abstração

> *"Mostrar apenas o essencial, esconder a complexidade."*

O GovFácil usa abstração em duas classes que **não podem ser instanciadas diretamente**:

**`Servico` (classe abstrata):**
Define que todo serviço *deve ter* `processar()` e `calcularPrazo()`, mas não implementa esses métodos — obriga as subclasses a implementarem de acordo com suas regras específicas. O cidadão interage com o conceito genérico de "serviço" sem precisar conhecer os detalhes internos de cada um.

**`Notificacao` (classe abstrata):**
Define que toda notificação *deve ter* `enviar()`, mas cada tipo de notificação decide o conteúdo e o formato. O sistema envia notificações sem precisar saber se é uma confirmação ou um lembrete.

**Benefício:** O sistema é extensível — para adicionar um novo tipo de serviço (ex: `Alvara`), basta criar uma nova classe filha de `Servico` e implementar os métodos abstratos. Nenhuma outra parte do código precisa ser modificada.

---

## 7. Fluxo Principal do Sistema

```
[Cidadão acessa o sistema]
        ↓
[Faz login com CPF e senha]
        ↓
[Escolhe um serviço disponível]
        ↓
[Preenche os dados e abre a solicitação]
        ↓
[Sistema gera número de protocolo automaticamente]
        ↓
[Notificação de confirmação é enviada ao cidadão]
        ↓
[Servidor recebe a solicitação no painel administrativo]
        ↓
[Servidor analisa, aprova ou rejeita]
        ↓
[Notificação de atualização de status é enviada ao cidadão]
        ↓
[Cidadão acompanha o andamento pelo número de protocolo]
        ↓
[Solicitação é concluída — registrada no histórico do cidadão]
```

---

## 8. Resumo dos Conceitos POO Aplicados

| Pilar | Onde | Como |
|---|---|---|
| **Encapsulamento** | `Usuario`, `Solicitacao` | Atributos privados (`_senha`, `_cpf`, `_status`) com acesso controlado por métodos |
| **Herança** | `Cidadao`, `Servidor`, todos os subtipos de `Servico` e `Notificacao` | Subclasses herdam atributos e métodos da classe pai e adicionam o que é específico |
| **Polimorfismo** | `processar()` em Servico, `enviar()` em Notificacao | O mesmo método produz comportamentos diferentes em cada subclasse |
| **Abstração** | `Servico`, `Notificacao` | Classes que definem o contrato sem implementação — forçam as subclasses a especializarem |

---

*Documentação elaborada para a atividade de Programação Orientada a Objetos — ADS*
