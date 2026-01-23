# API Bancária (bank_api)

## Descrição concisa

Projeto Python que fornece uma API REST para gerenciamento bancário simples: contas, autenticação de usuários, transações e cálculos de impostos. A API foi construída com FastAPI e SQLAlchemy para facilitar desenvolvimento rápido, testes e deploy.

## Funcionalidades principais

- Criação, consulta e gerenciamento de contas de usuário.
- Autenticação e geração de tokens (rota de login).
- Registro e consulta de transações (transferências, débitos/créditos).
- Mecanismos básicos de cálculo de tarifas/impostos.
- Endpoints para verificação de saúde da aplicação.

## Tecnologias

- Python 3.10+
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Alembic (migrações de schema)
- SQLite/Postgres (configurável via `db/session.py`)

## Estrutura do projeto

- `main.py` — entrada da aplicação e configuração do lifespan.
- `routes/` — definição dos endpoints (accounts, login, transactions).
- `models/` — modelos SQLAlchemy para banco de dados.
- `schemas/` — Pydantic schemas para validação/serialização.
- `services/` — lógica de negócio e regras (contas, taxas, transações).
- `db/` — configuração da sessão e base do banco.
- `alembic/` — scripts e histórico de migrações.
- `tests/` — testes automatizados (integração/unitários).

## Instalação

1. Criar e ativar um virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

## Uso rápido

Executar a aplicação localmente:

```bash
uvicorn main:app --reload
```

A documentação automática estará disponível em `http://127.0.0.1:8000/docs`.

## Testes

Executar os testes com pytest:

```bash
pytest -q
```

## Contribuição

Contribuições são bem-vindas. Abra issues para discutir mudanças grandes e envie pull requests pequenos e focados. Certifique-se de que os testes passam antes de submeter.
