# TaskTracker - Bootcamp II

Aplicação de linha de comando para cadastrar e consultar tarefas com prioridade, data limite e status.

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
└── src/
    └── main.py
```

## Instalação e execução

Não há dependências externas. Com Python 3 instalado, na raiz do projeto execute:

```bash
python src/main.py
```

Em alguns sistemas, use `python3 src/main.py`.

## Como usar

No menu, escolha `1` para cadastrar uma tarefa, `2` para listar as tarefas cadastradas ou `3` para sair. O título não pode ficar vazio. A prioridade aceita Alta, Média (ou Media) e Baixa. As tarefas ficam em memória enquanto o programa está aberto.

## Planejamento

O documento de planejamento lógico entregue na Fase 1 está preservado em `docs/planejamento_logico.pdf`.
