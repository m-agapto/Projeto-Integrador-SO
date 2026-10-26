import shutil
import time
from datetime import datetime
from pathlib import Path

# Ações predefinidas e portáveis. Nenhum comando digitado pelo usuário é executado.
ALLOWED_ACTIONS = {
    "date_time": "Registrar data e hora",
    "disk_usage": "Consultar espaço em disco",
    "project_directory": "Verificar diretório pessoal",
    "file_report": "Gerar relatório de arquivos de teste",
}


def execute_action(action, log_dir, timeout=20):
    """Executa uma ação segura usando APIs Python, tanto no Windows quanto no Linux."""
    del timeout  # Mantido por compatibilidade com a interface do agendador.
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    stdout, stderr, exit_code = "", "", 0

    try:
        if action == "date_time":
            stdout = f"Data e hora local: {datetime.now().astimezone().isoformat(timespec='seconds')}\n"
        elif action == "disk_usage":
            usage = shutil.disk_usage(log_dir)
            gib = 1024 ** 3
            stdout = (
                f"Unidade/diretório: {log_dir.resolve()}\n"
                f"Total: {usage.total / gib:.2f} GiB\n"
                f"Usado: {(usage.total - usage.free) / gib:.2f} GiB\n"
                f"Livre: {usage.free / gib:.2f} GiB\n"
            )
        elif action == "project_directory":
            home = Path.home()
            if not home.is_dir():
                raise OSError(f"Diretório pessoal não encontrado: {home}")
            stdout = f"Diretório pessoal acessível: {home}\n"
        elif action == "file_report":
            test_dir = log_dir / "sample_files"
            test_dir.mkdir(parents=True, exist_ok=True)
            sample = test_dir / "exemplo.txt"
            if not sample.exists():
                sample.write_text(
                    "Arquivo de exemplo para o Agendador Web.\n", encoding="utf-8"
                )
            files = sorted(item for item in test_dir.iterdir() if item.is_file())
            stdout = f"Relatório de arquivos em: {test_dir.resolve()}\n"
            for item in files:
                stdout += f"{item.name} ({item.stat().st_size} bytes)\n"
            if not files:
                stdout += "Nenhum arquivo encontrado.\n"
        else:
            raise ValueError("Ação não autorizada.")
    except Exception as exc:
        exit_code = 1
        stderr = f"{type(exc).__name__}: {exc}"

    duration = time.monotonic() - started
    return {
        "status": "concluída" if exit_code == 0 else "falhou",
        "exit_code": exit_code,
        "stdout": stdout[-12000:],
        "stderr": stderr[-12000:],
        "duration": round(duration, 3),
    }
