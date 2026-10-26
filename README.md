# Agendador Web de Tarefas — Windows e Linux

Aplicação web local em Flask para cadastrar tarefas predefinidas, agendar execução única ou recorrente, e consultar histórico, resultados e falhas. A versão agora funciona tanto no **Windows 10/11** quanto no Linux, usando APIs portáveis do Python em vez de depender de comandos exclusivos do Linux.

## Funcionalidades

- Painel com resumo de tarefas e execuções.
- Cadastro de execução única ou recorrência por intervalo.
- Ações seguras predefinidas: registrar data/hora, consultar espaço em disco, verificar diretório pessoal e gerar relatório de arquivos de teste.
- Pausar, reativar e cancelar tarefas futuras.
- Histórico de execução com saída, erros, duração e código de saída.
- Registro de eventos, pesquisa e exportação do histórico em CSV.
- Interface responsiva em português e banco SQLite local.

## Instalação no Windows 10/11

1. Instale **Python 3.10 ou superior** em [python.org](https://www.python.org/downloads/windows/). Marque a opção **Add python.exe to PATH** durante a instalação.
2. Extraia o ZIP para uma pasta normal, por exemplo `C:\Projetos\agendador-web`.
3. Abra PowerShell nessa pasta (no Explorador de Arquivos, clique na barra de endereço, digite `powershell` e pressione Enter).
4. Execute o instalador:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_windows.ps1
```

5. Inicie o sistema clicando duas vezes em `iniciar_windows.bat`, ou no PowerShell execute:

```powershell
.\iniciar_windows.bat
```

6. Abra `http://127.0.0.1:5000` no navegador. Para encerrar o servidor, volte à janela do terminal e pressione `Ctrl+C`.

Se a instalação do Flask falhar, verifique a conexão com a internet e execute novamente o instalador. O PowerShell não precisa reconhecer o comando `bash` nesta versão.

## Instalação no Linux / WSL

É necessário Python 3.10+ e conexão à internet para instalar o Flask:

```bash
bash scripts/setup.sh
source .venv/bin/activate
flask --app run.py run --debug
```

Abra `http://127.0.0.1:5000`.

## Testes

Windows (PowerShell):

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Linux:

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
```

## Como funciona

- **Flask** entrega as páginas web localmente.
- **SQLite** guarda tarefas, execuções e eventos.
- Um worker em segundo plano verifica tarefas vencidas a cada dois segundos.
- **Python `subprocess` não é usado para executar comandos arbitrários**: as quatro ações são implementadas com APIs Python, evitando depender de `bash`, `df` ou `find`.
- Os agendamentos e o histórico ficam na pasta `instance` do projeto.

## Segurança e limitações

- O sistema não permite que o usuário digite comandos arbitrários para execução.
- Esta é uma versão acadêmica para uso local. Não exponha o servidor de desenvolvimento à internet; não há autenticação multiusuário nem proteção CSRF completa.
- O agendador funciona dentro do processo web. Se o programa estiver fechado ou o computador desligado, tarefas não serão executadas nesse período. O histórico é salvo, mas não há garantia de execução pontual durante a indisponibilidade.
- O horário enviado pelo formulário é interpretado como UTC nesta versão inicial; isso pode diferir do horário local em algumas configurações.
- Cancelar ou pausar uma tarefa impede futuras execuções, mas não interrompe uma execução que já começou.

## Estrutura principal

```text
agendador-web-linux/
├── app/                  # Aplicação Flask, banco, agendador e interface
├── scripts/setup.sh      # Instalação Linux
├── scripts/setup_windows.ps1
├── iniciar_windows.bat   # Inicialização no Windows
├── tests/                # Testes automatizados
├── requirements.txt
└── run.py
```

## Próximas melhorias

Autenticação, proteção CSRF completa, fuso horário configurável, worker separado e persistente, limites de concorrência, cancelamento de processos em execução e testes de integração contínua.

## Status

MVP acadêmico em desenvolvimento.
