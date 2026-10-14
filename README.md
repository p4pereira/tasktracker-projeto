# TaskTracker - Bootcamp II

Aplicação de linha de comando para cadastrar, consultar, filtrar e gerenciar tarefas. Os dados ficam salvos localmente em JSON e continuam disponíveis ao reabrir o programa.

## Tecnologias

- Python 3.10 ou superior
- Biblioteca padrão do Python

## Estrutura

```text
tasktracker-projeto/
├── README.md
├── .gitignore
├── docs/
│   └── planejamento_logico.pdf
├── src/
│   └── main.py
└── tarefas.json  # criado automaticamente ao salvar a primeira tarefa
```

## Instalação e execução

Não há dependências externas. Com Python 3 instalado, na raiz do projeto execute:

```bash
python src/main.py
```

Em alguns sistemas, use `python3 src/main.py`.

## Como usar

No menu, escolha:

1. Cadastrar tarefa. O título é obrigatório; prioridades aceitas: Alta, Média (ou Media) e Baixa. A data pode ser livre ou uma data válida no formato DD/MM/AAAA.
2. Listar todas as tarefas.
3. Alternar o status entre Pendente e Concluída ou excluir uma tarefa (com confirmação).
4. Filtrar tarefas por prioridade ou status.
5. Sair.

As alterações são salvas automaticamente em `tarefas.json`. Se o JSON estiver inválido ou não seguir o formato esperado, uma cópia de segurança com o sufixo `.corrompido-<data>` é preservada antes de iniciar uma lista vazia.

## Planejamento

O documento de planejamento lógico entregue na Fase 1 está preservado em `docs/planejamento_logico.pdf`.
