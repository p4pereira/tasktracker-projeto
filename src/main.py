"""TaskTracker: cadastro e listagem de tarefas pela linha de comando."""


def solicitar_titulo(input_fn=input, print_fn=print):
    """Solicita um título não vazio, repetindo até receber um valor válido."""
    while True:
        titulo = input_fn("Título: ").strip()
        if titulo:
            return titulo
        print_fn("O título é obrigatório e não pode conter apenas espaços. Tente novamente.")


def solicitar_prioridade(input_fn=input, print_fn=print):
    """Solicita uma prioridade válida e a normaliza para apresentação."""
    opcoes = {"alta": "Alta", "média": "Média", "media": "Média", "baixa": "Baixa"}
    while True:
        prioridade = input_fn("Prioridade (Alta, Média ou Baixa): ").strip().casefold()
        if prioridade in opcoes:
            return opcoes[prioridade]
        print_fn("Prioridade inválida. Informe Alta, Média (ou Media) ou Baixa.")


def cadastrar_tarefa(tarefas, input_fn=input, print_fn=print):
    """Lê os dados de uma tarefa e a adiciona à lista."""
    print_fn("\nCadastro de tarefa")
    titulo = solicitar_titulo(input_fn, print_fn)
    descricao = input_fn("Descrição: ").strip()
    prioridade = solicitar_prioridade(input_fn, print_fn)
    data_limite = input_fn("Data limite (formato livre ou DD/MM/AAAA): ").strip()
    tarefas.append({
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": "Pendente",
    })
    print_fn("Tarefa cadastrada com sucesso.")


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


def exibir_menu(print_fn=print):
    print_fn("\n=== TaskTracker ===")
    print_fn("1. Cadastrar nova tarefa")
    print_fn("2. Visualizar tarefas cadastradas")
    print_fn("3. Sair da aplicação")


def executar(input_fn=input, print_fn=print):
    """Executa o menu até a opção de saída."""
    tarefas = []
    while True:
        exibir_menu(print_fn)
        opcao = input_fn("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_tarefa(tarefas, input_fn, print_fn)
        elif opcao == "2":
            listar_tarefas(tarefas, print_fn)
        elif opcao == "3":
            print_fn("Encerrando o TaskTracker. Até mais!")
            return
        else:
            print_fn("Opção inválida. Escolha 1, 2 ou 3.")


if __name__ == "__main__":
    try:
        executar()
    except (EOFError, KeyboardInterrupt):
        print("\nAplicação encerrada.")
