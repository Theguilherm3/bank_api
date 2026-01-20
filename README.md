# Data Bank API

API REST para controle simples de contas e transações financeiras (entradas e saídas), construída com **FastAPI** e **SQLAlchemy**, usando **SQLite** como banco local e **Alembic** para migrações.

> Ambiente alvo: Windows (PowerShell)

---

## Sumário

- Visão geral
- Funcionalidades
- Stack e requisitos
- Como rodar (desenvolvimento)
- Banco de dados e migrações (Alembic)
- Regras de negócio
- Endpoints (com exemplos)
- Estrutura do projeto
- Troubleshooting (erros comuns)

---

## Visão geral

O projeto expõe endpoints para:

- Criar uma conta com saldo inicial
- Consultar saldo e dados de uma conta
- Criar transações (entrada/saída) vinculadas a uma conta
- Listar transações de uma conta

O saldo da conta é calculado dinamicamente a partir das transações:

- `ENTRADA` soma no saldo
- `SAIDA` subtrai do saldo

---

## Funcionalidades

- Health check (`/health`)
- Cadastro de conta com número de 4 dígitos (1000–9999)
- Lançamento de transações por conta
- Listagem de transações ordenadas por data (desc)
- Validação de payloads via Pydantic
- Migrações com Alembic

---

## Stack e requisitos

- Python (requer `>= 3.13`, conforme `pyproject.toml`)
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn
- SQLite (arquivo local)

---

## Como rodar (desenvolvimento)

1. Instalar dependências:

```powershell
uv sync
```

2. Rodar a API:

```powershell
uv run uvicorn main:app --reload
```

A aplicação ficará disponível em:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Banco de dados e migrações (Alembic)

- Banco: SQLite local
- Arquivo padrão: `objectivebank.db`
- URL no Alembic: `sqlite:///./objectivebank.db` (em `alembic.ini`)

### Aplicar migrações

```powershell
alembic upgrade head
```

### Criar uma nova migração

```powershell
alembic revision --autogenerate -m "descricao_da_migracao"
```

### Guia rápido

Veja: `PASSOS_ALEMBIC.markdown`

---

## Regras de negócio

### Tipos de movimento (`movment_type`)

Enum `EnumMovmentType`:

- `ENTRADA`
- `SAIDA`

### Tipos de pagamento (`transaction_type`)

Enum `EnumPaymentTypes`:

- `P` (PIX)
- `C` (CRÉDITO)
- `D` (DÉBITO)

### Saldo

O saldo é calculado a partir das transações:

$$
saldo = \sum entradas - \sum saidas
$$

---

## Endpoints (com exemplos)

Base URL (local): `http://127.0.0.1:8000`

### Health check

**GET** `/health`

Resposta (200):

```json
{ "ok": true, "status": "running" }
```

---

## Contas

### Criar conta

**POST** `/conta/criar`

Body:

```json
{
  "username": "Seu Nome",
  "balance": 6025.54
}
```

Resposta (200):

```json
{
  "id": 1,
  "username": "Seu Nome",
  "account_number": 1234,
  "balance": 6025.54
}
```

PowerShell (cURL):

```powershell
curl -X POST "http://127.0.0.1:8000/conta/criar" `
	-H "Content-Type: application/json" `
	-d "{\"username\":\"Seu Nome\",\"balance\":6025.54}"
```

Observação:

- Ao criar a conta, o sistema cria uma transação inicial de `ENTRADA` com tipo `P` (PIX) no valor do saldo inicial.

### Consultar conta e saldo

**GET** `/conta?account_number=1234`

PowerShell (cURL):

```powershell
curl "http://127.0.0.1:8000/conta?account_number=1234"
```

---

## Transações

### Criar transação

**POST** `/transacao`

Body:

```json
{
  "movment_type": "SAIDA",
  "transaction_type": "D",
  "account_id": 1234,
  "amount": 129.97
}
```

PowerShell (cURL):

```powershell
curl -X POST "http://127.0.0.1:8000/transacao" `
	-H "Content-Type: application/json" `
	-d "{\"movment_type\":\"SAIDA\",\"transaction_type\":\"D\",\"account_id\":1234,\"amount\":129.97}"
```

### Listar transações de uma conta

**GET** `/transacao/all?account_number=1234`

Resposta (200) - exemplo:

```json
[
  {
    "id": 10,
    "movment_type": "SAIDA",
    "transaction_type": "D",
    "amount": 129.97,
    "date": "2026-01-20"
  }
]
```

PowerShell (cURL):

```powershell
curl "http://127.0.0.1:8000/transacao/all?account_number=1234"
```

---

## Estrutura do projeto

```text
.
├─ main.py                # inicialização da API e inclusão das rotas
├─ db/
│  ├─ base.py             # Base declarativa do SQLAlchemy
│  └─ session.py          # engine e SessionLocal
├─ models/                # models SQLAlchemy (Account, Transactions) e enums
├─ schemas/               # schemas Pydantic
├─ routes/                # rotas FastAPI
├─ services/              # regras de negócio / acesso ao banco
├─ alembic/               # migrações
├─ alembic.ini
└─ objectivebank.db       # arquivo do SQLite local
```
