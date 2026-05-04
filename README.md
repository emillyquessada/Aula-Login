# Configurar o alembic
Inicie o alembic

no terminal: 
```bash
python -m alembic init migrations
```
### Edite o arquivo alembic.ini na linha 89 e deixe assim:
sqlalchemy.url =

### Depois edite o arquivo migrations/env.py
### Rodar o alembic - criar uma migrations
```bash
python -m alembic revision --autogenerate -m "Criar tabela usuário"
```
#Aplique a migration
```bash
python -m alembic upgrade head
```