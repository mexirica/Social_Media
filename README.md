
# Instagram "Clone"

Rede social feita em Django com funções de CRUD, autenticação e autorização, followers, etc.


## Venv

Criação do ambiente virtual

```bash
  python -m venv venv
```

Para a inicialização do ambiente (Se Windows)

```bash
  venv/Scripts/Activate
```
Para a inicialização do ambiente (Se Linux/Mac)

```bash
  source venv/bin/activate
```

Instalação dos pacotes necessários

```bash
  pip install -r requirements.txt
```

Após esses passos é possível rodar o main do programa.

## Instalação Django

Para a instalação do projeto
```bash
    py manage.py migrate
```

Criação de um super user (Não necessário por ora)
```bash
    py manage.py createsuperuser
```

Inicializar server
```bash
    py manage.py runserver
```
