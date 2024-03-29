import requests
from bs4 import BeautifulSoup
import sys
import os

if len(sys.argv) > 1:
    url_base = sys.argv[1]  # Recebe a URL base como argumento do código principal
else:
    print("URL base não foi fornecida.")
    sys.exit(1)

# Construir a URL alvo usando a URL base e o nome da página
url_alvo = f"{url_base}/index.php?page=user-poll.php"
print(url_alvo)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Payloads para testar
payloads = {
    'Parameter Pollution': "&choice=nmap&choice=wireshark",
    'XSS': "&choice=<script>alert('XSS')</script>",
    'CSRF': "&choice=nmap&csrf-token=CSRFToken123",
    'HTML Injection': "&choice=<b>HTML<b>Injection"
}

# Função para enviar a requisição e verificar a resposta
def enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, teste_numero):
    resposta_teste = requests.get(url_completa, headers=headers)
    soup = BeautifulSoup(resposta_teste.text, 'html.parser')
    titulo = soup.find('title').text if soup.find('title') else ''

    print(f"Teste {teste_numero}: Testando '{tipo_vulnerabilidade}'. Título: {titulo[:46]}")
    
    if titulo != "Acesso Bloqueado":
        print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
        return 1  # Retornar 1 se o teste passou
    else:
        print(f"Teste #{teste_numero} FALHOU: Acesso bloqueado.")
        return 0  # Retornar 0 se o teste falhou

# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for tipo_vulnerabilidade, payload in payloads.items():
    total_testes += 1  # Incrementar o contador total de testes
    url_completa = f"{url_alvo}&csrf-token=&initials=&user-poll-php-submit-button=Submit+Vote{payload}"
    resultado_teste = enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, total_testes)
    if resultado_teste == 1:
        testes_passaram += 1
    else:
        testes_falharam += 1

# Reportar os resultados finais
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")
print(f"Url Testada: {url_alvo}") #Depurar e informar a url final que foi alvo