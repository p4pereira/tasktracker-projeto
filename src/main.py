"""TaskTracker: gerenciador de tarefas persistente pela linha de comando."""

import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path


PRIORIDADES = {"alta": "Alta", "média": "Média", "media": "Média", "baixa": "Baixa"}
STATUS_VALIDOS = {"pendente": "Pendente", "concluída": "Concluída", "concluida": "Concluída"}
ARQUIVO_TAREFAS = Path(__file__).resolve().parent.parent / "tarefas.json"


def _normalizar_tarefa(dados):
    """Valida e normaliza um registro carregado do arquivo JSON."""
    if not isinstance(dados, dict):
        raise ValueError("registro não é um objeto")

    titulo = dados.get("titulo")
    prioridade = dados.get("prioridade")
    status = dados.get("status")
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("título ausente ou inválido")
    if not isinstance(prioridade, str) or prioridade.strip().casefold() not in PRIORIDADES:
        raise ValueError("prioridade ausente ou inválida")
    if not isinstance(status, str) or status.strip().casefold() not in STATUS_VALIDOS:
        raise ValueError("status ausente ou inválido")

    descricao = dados.get("descricao", "")
    data_limite = dados.get("data_limite", "")
    if not isinstance(descricao, str) or not isinstance(data_limite, str):
        raise ValueError("descrição ou data limite inválida")
    return {
        "titulo": titulo.strip(),
        "descricao": descricao.strip(),
        "prioridade": PRIORIDADES[prioridade.strip().casefold()],
        "data_limite": data_limite.strip(),
        "status": STATUS_VALIDOS[status.strip().casefold()],
    }


def carregar_tarefas(caminho=ARQUIVO_TAREFAS, print_fn=print):
    """Carrega tarefas. Se o JSON estiver inválido, preserva-o em um backup."""
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if not isinstance(dados, list):
            raise ValueError("a raiz do JSON deve ser uma lista")
        return [_normalizar_tarefa(tarefa) for tarefa in dados]
    except (OSError, json.JSONDecodeError, ValueError) as erro:
        backup = caminho.with_name(f"{caminho.name}.corrompido-{datetime.now():%Y%m%d-%H%M%S}")
        try:
            shutil.copy2(caminho, backup)
            caminho.unlink()
            print_fn(f"Arquivo de tarefas inválido ({erro}). Cópia preservada em: {backup.name}")
        except OSError as backup_erro:
            raise RuntimeError(
                f"Não foi possível preservar o arquivo inválido ({backup_erro}); "
                "a aplicação foi interrompida para evitar perda de dados."
            ) from backup_erro
        return []


def salvar_tarefas(tarefas, caminho=ARQUIVO_TAREFAS):
    """Salva tarefas de forma atômica para reduzir risco de arquivo incompleto."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=caminho.parent,
            prefix=f".{caminho.name}.", suffix=".tmp", delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
            arquivo.flush()
            os.fsync(arquivo.fileno())
        temporario.replace(caminho)
    finally:
        if temporario is not None and temporario.exists():
            temporario.unlink()


def solicitar_titulo(input_fn=input, print_fn=print):
    """Solicita um título não vazio, repetindo até receber um valor válido."""
    while True:
        titulo = input_fn("Título: ").strip()
        if titulo:
            return titulo
        print_fn("O título é obrigatório e não pode conter apenas espaços. Tente novamente.")


def solicitar_prioridade(input_fn=input, print_fn=print):
    """Solicita uma prioridade válida e a normaliza para apresentação."""
    while True:
        valor = input_fn("Prioridade (Alta, Média ou Baixa): ").strip().casefold()
        if valor in PRIORIDADES:
            return PRIORIDADES[valor]
        print_fn("Prioridade inválida. Informe Alta, Média (ou Media) ou Baixa.")


def solicitar_data_limite(input_fn=input, print_fn=print):
    """Aceita data livre ou valida datas informadas no formato DD/MM/AAAA."""
    while True:
        data = input_fn("Data limite (livre ou DD/MM/AAAA): ").strip()
        if not data:
            return ""
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            if len(data) == 10 and data[2] == "/" and data[5] == "/":
                print_fn("Data inválida. Use uma data válida no formato DD/MM/AAAA ou uma descrição livre.")
                continue
        return data


def cadastrar_tarefa(tarefas, input_fn=input, print_fn=print, salvar_fn=salvar_tarefas):
    """Lê os dados de uma tarefa, salva e adiciona o novo registro."""
    print_fn("\nCadastro de tarefa")
    tarefa = {
        "titulo": solicitar_titulo(input_fn, print_fn),
        "descricao": input_fn("Descrição (opcional): ").strip(),
        "prioridade": solicitar_prioridade(input_fn, print_fn),
        "data_limite": solicitar_data_limite(input_fn, print_fn),
        "status": "Pendente",
    }
    tarefas.append(tarefa)
    salvar_fn(tarefas)
    print_fn("Tarefa cadastrada e salva com sucesso.")


def listar_tarefas(tarefas, print_fn=print):
    """Exibe todas as tarefas ou informa que a lista está vazia."""
    if not tarefas:
        print_fn("Ainda não existem tarefas cadastradas.")
        return
    print_fn("\nTarefas cadastradas")
    for indice, tarefa in enumerate(tarefas, start=1):
        print_fn(f"\n{indice}. {tarefa['titulo']}")
        print_fn(f"   Descrição: {tarefa['descricao'] or '(sem descrição)'}")
        print_fn(f"   Prioridade: {tarefa['prioridade']}")
        print_fn(f"   Data limite: {tarefa['data_limite'] or '(não informada)'}")
        print_fn(f"   Status: {tarefa['status']}")


def _solicitar_indice(tarefas, input_fn, print_fn):
    """Solicita índice numérico válido de tarefa; retorna None ao cancelar."""
    valor = input_fn("Número da tarefa (ou 0 para voltar): ").strip()
    if valor == "0":
        return None
    if not valor.isdigit() or not 1 <= int(valor) <= len(tarefas):
        print_fn("Número inválido. Escolha uma tarefa existente ou 0 para voltar.")
        return None
    return int(valor) - 1


def gerenciar_tarefa(tarefas, input_fn=input, print_fn=print, salvar_fn=salvar_tarefas):
    """Alterna o status de uma tarefa ou a remove após confirmação."""
    if not tarefas:
        print_fn("Não há tarefas para gerenciar.")
        return
    listar_tarefas(tarefas, print_fn)
    indice = _solicitar_indice(tarefas, input_fn, print_fn)
    if indice is None:
        return
    tarefa = tarefas[indice]
    print_fn("1. Alternar status (Pendente/Concluída)")
    print_fn("2. Excluir tarefa")
    print_fn("3. Voltar")
    opcao = input_fn("Escolha uma opção: ").strip()
    if opcao == "1":
        tarefa["status"] = "Concluída" if tarefa["status"] == "Pendente" else "Pendente"
        salvar_fn(tarefas)
        print_fn(f"Status atualizado para {tarefa['status']}.")
    elif opcao == "2":
        confirmacao = input_fn(f"Confirma excluir '{tarefa['titulo']}'? (s/n): ").strip().casefold()
        if confirmacao == "s":
            removida = tarefas.pop(indice)
            salvar_fn(tarefas)
            print_fn(f"A tarefa '{removida['titulo']}' foi removida.")
        else:
            print_fn("Exclusão cancelada.")
    elif opcao != "3":
        print_fn("Opção inválida. Nenhuma alteração foi feita.")


def filtrar_tarefas(tarefas, input_fn=input, print_fn=print):
    """Filtra por prioridade ou status com validação estrita das opções."""
    if not tarefas:
        print_fn("Não há tarefas para filtrar.")
        return
    print_fn("\nFiltrar tarefas")
    print_fn("1. Por prioridade")
    print_fn("2. Por status")
    print_fn("3. Voltar")
    opcao = input_fn("Escolha uma opção: ").strip()
    if opcao == "1":
        prioridade = solicitar_prioridade(input_fn, print_fn)
        encontradas = [t for t in tarefas if t["prioridade"] == prioridade]
    elif opcao == "2":
        print_fn("1. Pendente")
        print_fn("2. Concluída")
        status_opcao = input_fn("Status desejado: ").strip()
        if status_opcao not in {"1", "2"}:
            print_fn("Status inválido. Escolha 1 ou 2.")
            return
        status = "Pendente" if status_opcao == "1" else "Concluída"
        encontradas = [t for t in tarefas if t["status"] == status]
    elif opcao == "3":
        return
    else:
        print_fn("Opção inválida. Escolha 1, 2 ou 3.")
        return
    if encontradas:
        listar_tarefas(encontradas, print_fn)
    else:
        print_fn("Nenhuma tarefa encontrada para esse filtro.")


def exibir_menu(print_fn=print):
    print_fn("\n=== TaskTracker ===")
    print_fn("1. Cadastrar nova tarefa")
    print_fn("2. Visualizar todas as tarefas")
    print_fn("3. Gerenciar tarefa (status ou excluir)")
    print_fn("4. Filtrar tarefas")
    print_fn("5. Sair da aplicação")


def executar(input_fn=input, print_fn=print, caminho=ARQUIVO_TAREFAS):
    """Executa o menu até a opção de saída, carregando e salvando JSON."""
    tarefas = carregar_tarefas(caminho, print_fn)
    while True:
        exibir_menu(print_fn)
        opcao = input_fn("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_tarefa(tarefas, input_fn, print_fn, lambda dados: salvar_tarefas(dados, caminho))
        elif opcao == "2":
            listar_tarefas(tarefas, print_fn)
        elif opcao == "3":
            gerenciar_tarefa(tarefas, input_fn, print_fn, lambda dados: salvar_tarefas(dados, caminho))
        elif opcao == "4":
            filtrar_tarefas(tarefas, input_fn, print_fn)
        elif opcao == "5":
            print_fn("Encerrando o TaskTracker. Até mais!")
            return
        else:
            print_fn("Opção inválida. Escolha 1, 2, 3, 4 ou 5.")


if __name__ == "__main__":
    try:
        executar()
    except (EOFError, KeyboardInterrupt):
        print("\nAplicação encerrada.")
