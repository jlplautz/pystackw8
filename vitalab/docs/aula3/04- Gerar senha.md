Em utils.py vamos criar um função que gera uma senha aleatória:
```bash
from random import choice, shuffle
import string

def gerar_senha_aleatoria(tamanho):

    caracteres_especiais = string.punctuation   
    caracteres = string.ascii_letters
    numeros_list = string.digits

    
    sobra = 0
    qtd = tamanho // 3
    if not tamanho % 3 == 0:
        sobra = tamanho - qtd

    letras = ''
    for i in range(0, qtd + sobra):
        letras += choice(caracteres)

    numeros = ''
    for i in range(0, qtd):
        numeros += choice(numeros_list)

    especiais = ''
    for i in range(0, qtd):
        especiais += choice(caracteres_especiais)

    
    senha = list(letras + numeros + especiais)
    shuffle(senha)

    return ''.join(senha)
```
# ATENÇÃO, QUEM ESTÁ NO WINDOWS FAÇA O SEGUINTE PRIMEIRO.

# INSTALE O GTK3, ACESSANDO O SITE:

```bash
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
```

# Instale o executável baixado.

# Reinicie sua máquina e depois de continuidade no processo

```bash
pip install weasyprint
```


Em templates/partials crie o modelo do arquivo senha_exame.html para ser impresso:
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
    <div>

        <h3>Exame: {{exame}}</h3>
        <h3>Paciente: {{paciente}}</h3>
        <hr>
        <h3>Senha: {{senha}}</h3>

    </div>

</body>
</html>
```

Agora crie a função que cria um PDF e salva em memória:
```bash
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML

def gerar_pdf_exames(exame, paciente, senha):

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/senha_exame.html')
    template_render = render_to_string(path_template, {'exame': exame, 'paciente': paciente, 'senha': senha})

    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return path_output
```

Crie a URL para gerar a senha:
```bash
path('gerar_senha/<int:exame_id>', views.gerar_senha, name="gerar_senha"),
```
E seu view:
```bash
@staff_member_required 
def gerar_senha(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    if exame.senha:
        # Baixar o documento da senha já existente
        return FileResponse(gerar_pdf_exames(exame.exame.nome, exame.usuario, exame.senha), filename="token.pdf")
    
    senha = gerar_senha_aleatoria(9)
    exame.senha = senha
    exame.save()
    return FileResponse(gerar_pdf_exames(exame.exame.nome, exame.usuario, exame.senha), filename="token.pdf")
```

No botão Gerar senha de exame_cliente.html redireciona para URL criada:
```bash
<a style="text-decoration: none;" href="{% url "gerar_senha" exame.id %}" class="btn-secundario">Gerar senha</a>
```
