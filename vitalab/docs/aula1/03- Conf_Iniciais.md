Primeiro devemos criar o ambiente virtual:
```bash
# Criar
# Linux
python3 -m venv venv
# Windows
python -m venv venv
```

Após a criação do venv vamos ativa-lo:
```bash
#Ativar
# Linux
source venv/bin/activate
# Windows
venv\Scripts\Activate
# Caso algum comando retorne um erro de permissão execute o código e tente novamente:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Agora vamos fazer a instalação do Django e as demais bibliotecas:
```bash
pip install django
pip install pillow
```

Vamos criar o nosso projeto Django:
```bash
django-admin startproject vitalab .
```

Rode o servidor para testar:
```bash
python manage.py runserver
```

Crie o app usuario:
```bash
python manage.py startapp usuarios
```