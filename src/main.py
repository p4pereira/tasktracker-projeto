tarefas = []


def menu():
    print("\n=== TaskTracker ===")
    print("1. Cadastrar nova tarefa")
    print("2. Visualizar tarefas cadastradas")
    print("3. Sair da aplicação")


def executar():
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            tarefa = {
                "titulo": input("Título: ").strip(),
                "descricao": input("Descrição: ").strip(),
                "prioridade": input("Prioridade: ").strip(),
                "data_limite": input("Data limite: ").strip(),
                "status": "Pendente",
            }
            tarefas.append(tarefa)
            print("Tarefa cadastrada.")
        elif opcao == "2":
            if not tarefas:
                print("Ainda não existem tarefas cadastradas.")
            for numero, tarefa in enumerate(tarefas, 1):
                print(f"{numero}. {tarefa}")
        elif opcao == "3":
            print("Encerrando o TaskTracker.")
            break
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")


if __name__ == "__main__":
    executar()
