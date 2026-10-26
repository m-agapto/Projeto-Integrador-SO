# Agendador Web de Tarefas Linux

Uma aplicação web para cadastrar, programar e acompanhar tarefas automatizadas em um ambiente Linux, sem exigir que o usuário escreva comandos diretamente no terminal. O sistema oferece uma interface centralizada para gerenciar execuções agendadas, consultar resultados e identificar falhas.

> **Objetivo:** simplificar a automação de tarefas administrativas no Linux e demonstrar, na prática, conceitos de Sistemas Operacionais, execução de processos, permissões, agendamento e registro de eventos.

## Problema que o projeto resolve

Tarefas como gerar relatórios, verificar espaço em disco ou organizar arquivos muitas vezes precisam ser executadas repetidamente. Configurá-las manualmente pelo terminal pode ser difícil para usuários iniciantes e dificulta o acompanhamento do histórico de execuções.

O Agendador Web de Tarefas Linux propõe uma interface gráfica acessível pelo navegador para configurar tarefas permitidas, definir quando devem ser executadas e consultar seus resultados em um único lugar.

## Funcionalidades

### 1. Cadastro e configuração de tarefas
- Criar uma tarefa com nome e descrição.
- Selecionar uma ação previamente autorizada pelo sistema.
- Configurar os parâmetros permitidos para a ação.
- Definir data e hora para uma execução única ou uma frequência recorrente.
- Consultar e editar as configurações de tarefas existentes.

### 2. Agendamento e controle
- Agendar tarefas para uma data e horário específicos.
- Configurar recorrências, como diariamente, semanalmente ou em intervalos definidos.
- Pausar e reativar tarefas recorrentes.
- Cancelar tarefas futuras.
- Visualizar o próximo horário previsto para execução.

### 3. Acompanhamento das execuções
- Exibir o estado de cada tarefa: agendada, em execução, concluída, falhou, pausada ou cancelada.
- Mostrar o horário de início e término, a duração e o código de saída.
- Consultar a saída produzida pela tarefa e as mensagens de erro.
- Manter um histórico das execuções anteriores.
- Pesquisar tarefas por nome, estado ou período.

### 4. Registro e relatórios
- Registrar eventos importantes, como criação, alteração, pausa, cancelamento e execução.
- Gerar relatórios simples sobre execuções bem-sucedidas e falhas.
- Exportar o histórico, por exemplo, em CSV.
- Informar quando uma tarefa falhar, permitindo que o usuário investigue o motivo.

### 5. Tarefas de exemplo
Para facilitar os testes e a demonstração, o sistema pode oferecer ações seguras predefinidas, como:
- Consultar o uso de espaço em disco.
- Registrar data e hora da execução.
- Verificar a disponibilidade de um diretório de teste.
- Gerar um relatório de arquivos de uma pasta autorizada.
- Executar um script Bash mantido pelo próprio projeto.

## Como o sistema funcionará

1. O usuário acessa o painel pelo navegador.
2. Cadastra uma tarefa e escolhe uma ação permitida.
3. Define o horário ou a frequência de execução.
4. A aplicação salva a configuração no banco de dados SQLite.
5. Um componente de agendamento identifica as tarefas que devem ser executadas.
6. O sistema inicia a ação autorizada como um processo no Linux.
7. A saída, os erros, o horário e o código de retorno são registrados.
8. O painel apresenta o resultado e mantém o histórico para consulta.

## Tecnologias previstas

| Tecnologia | Responsabilidade |
|---|---|
| Python | Lógica principal da aplicação |
| Flask | Servidor web e rotas da aplicação |
| SQLite | Armazenamento de tarefas e histórico |
| HTML | Estrutura das páginas |
| CSS | Estilização e adaptação da interface |
| JavaScript | Interações e atualização de informações no painel |
| Bash | Scripts de automação e apoio à execução no Linux |
| `cron` ou agendador próprio | Execução programada das tarefas, conforme a implementação escolhida |
| Git e GitHub | Versionamento e colaboração |

## Conceitos de Sistemas Operacionais demonstrados

- **Gerenciamento de processos:** iniciar tarefas, acompanhar seu estado e registrar o resultado da execução.
- **Agendamento:** executar tarefas em horários definidos e lidar com recorrências.
- **Permissões e segurança:** limitar as ações disponíveis e o acesso aos arquivos e diretórios.
- **Sistema de arquivos:** ler arquivos autorizados e salvar logs e relatórios.
- **Terminal e Shell Script:** utilizar scripts Bash para automatizar procedimentos.
- **Registro de eventos:** manter logs que permitam verificar o comportamento do sistema e diagnosticar falhas.
- **Códigos de saída:** distinguir uma execução bem-sucedida de uma execução que terminou com erro.

O projeto deverá demonstrar pelo menos três conceitos de Sistemas Operacionais, incluindo um relacionado a processos, arquivos, armazenamento ou recursos do sistema.

## Segurança

Como a aplicação pode iniciar processos no Linux, a segurança deve ser considerada desde o início.

- Não permitir que o usuário envie qualquer comando de terminal para execução livre.
- Utilizar uma lista de ações previamente autorizadas.
- Validar todos os parâmetros recebidos pelo formulário.
- Executar a aplicação com privilégios mínimos, sem usar `sudo` indiscriminadamente.
- Restringir o acesso a diretórios definidos para o projeto.
- Registrar quem solicitou uma ação e quando ela foi executada, caso haja autenticação.
- Evitar expor variáveis de ambiente, senhas, tokens ou outros dados sensíveis nos logs.
- Tratar cancelamentos e falhas sem deixar processos ou arquivos temporários abandonados.

## Automação com Shell Script

O repositório incluirá scripts Bash para apoiar a operação do sistema. Por exemplo, um script poderá preparar os diretórios necessários, iniciar a aplicação em ambiente de desenvolvimento ou executar uma tarefa autorizada e registrar seu resultado.

Os scripts deverão conter instruções de uso e tratamento básico de erros. A automação escolhida será documentada no README e demonstrada durante a apresentação.

## Testes e validação

Os testes deverão verificar, no mínimo, se:

- Uma tarefa pode ser cadastrada e consultada.
- Uma tarefa única é executada no horário previsto.
- Uma tarefa recorrente pode ser pausada e reativada.
- Uma tarefa cancelada não é iniciada posteriormente.
- O histórico registra o resultado e o código de saída.
- Uma falha é identificada e apresentada ao usuário.
- Parâmetros inválidos são rejeitados.
- Ações não autorizadas não podem ser executadas.
- O sistema continua funcionando após ser reiniciado, preservando os registros salvos no SQLite.

Os testes devem ser executados em um ambiente Linux documentado, como uma máquina virtual ou o WSL, quando compatível com a configuração adotada.

## Estrutura sugerida do repositório

```text
agendador-web-linux/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── scheduler.py
│   ├── task_runner.py
│   ├── database.py
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── scripts/
│   ├── setup.sh
│   └── exemplo_tarefa.sh
├── tests/
├── logs/
├── requirements.txt
├── .gitignore
└── README.md
```

A estrutura é uma sugestão inicial e pode ser adaptada conforme a implementação. Arquivos de log, banco de dados local, ambientes virtuais e segredos não devem ser enviados ao GitHub quando contiverem dados locais ou sensíveis.

## Escopo inicial (MVP)

A primeira versão deverá priorizar:

1. Criar e listar tarefas.
2. Disponibilizar algumas ações seguras predefinidas.
3. Agendar uma execução única e uma recorrente.
4. Executar a ação no Linux.
5. Registrar estado, horário, saída e erros.
6. Permitir pausar ou cancelar tarefas futuras.
7. Incluir pelo menos um script Bash funcional.
8. Documentar instalação, execução e testes.

Depois que o MVP estiver estável, poderão ser adicionados autenticação, níveis de acesso, notificações, exportação de relatórios, execução concorrente controlada e suporte a múltiplos usuários.

## Limitações e decisões de implementação

O projeto será desenvolvido inicialmente para um ambiente Linux controlado. A escolha entre utilizar `cron` e um agendador implementado na aplicação deverá ser definida durante o desenvolvimento: `cron` é adequado para agendamentos do sistema, enquanto um agendador próprio pode facilitar a integração com o banco de dados e o painel web.

A aplicação deverá lidar com reinicializações, tarefas perdidas e execuções duplicadas de forma documentada. O comportamento exato dependerá do mecanismo de agendamento escolhido.

## Resultado esperado

Ao final, o projeto deverá oferecer um painel web funcional para administrar tarefas autorizadas do Linux, acompanhar execuções e consultar um histórico confiável. A solução demonstrará como uma aplicação web pode interagir com recursos do sistema operacional de maneira controlada, segura e automatizada.

## Integrantes

- Nome do integrante 1
- Nome do integrante 2
- Nome do integrante 3

## Status do projeto

Planejamento / Em desenvolvimento
