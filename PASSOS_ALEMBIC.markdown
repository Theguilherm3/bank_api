# Passos para Configurar o Alembic com SQLAlchemy e Models Customizados

1. **Executar o comando de inicialização do Alembic:**
   ```
   alembic init alembic
   ```
   Isso cria a pasta `alembic/` e o arquivo `alembic.ini`.

2. **Configurar o caminho do banco de dados:**
   - No arquivo `alembic.ini`, edite a linha `sqlalchemy.url` para apontar para o seu banco de dados.
     Exemplo:
     ```ini
     sqlalchemy.url = sqlite:///./objectivebank.db
     ```

3. **Ajustar o arquivo `alembic/env.py`:**
   - Importe sua base de models e o objeto `Base`:
     ```python
     from db.base import Base
     from models import *  # Garante que todas as tabelas sejam registradas
     target_metadata = Base.metadata
     ```

4. **Garantir que o arquivo `models/__init__.py` importe explicitamente todos os models:**
   - Exemplo de `models/__init__.py`:
     ```python
     from .accounts import Account
     from .transactions import Transactions
     ```
   - Isso garante que, ao importar `models`, todas as tabelas sejam registradas no metadata.

5. **Gerar uma nova migration automaticamente:**
   ```
   alembic revision --autogenerate -m "Mensagem da migration"
   ```
   - O Alembic irá detectar as tabelas e gerar o script de migration.

6. **Aplicar as migrations ao banco de dados:**
   ```
   alembic upgrade head
   ```

---

## Resumo das alterações necessárias
- O arquivo `models/__init__.py` deve importar explicitamente todos os models.
- O arquivo `alembic/env.py` deve importar o `Base` e os models para que o Alembic reconheça as tabelas.
- Sempre rode o `alembic revision --autogenerate` após criar ou alterar models.

Pronto! Agora o Alembic irá reconhecer e migrar suas tabelas corretamente.