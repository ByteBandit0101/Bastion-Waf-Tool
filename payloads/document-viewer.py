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
url_alvo = f"{url_base}/index.php?page=document-viewer.php"
print(url_alvo)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# Payloads para testar
payloads = {
    'Cross Site Scripting': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'HTTP Parameter Pollution': "valid_file.pdf&file=malicious_file.txt",
    'Frame Source Injection': "<iframe src='http://malicious.com'></iframe>",
}
# Função assíncrona para enviar a requisição e verificar a resposta
async def enviar_requisicao_e_verificar_resposta(payload, tipo_vulnerabilidade, teste_numero):
    url_completa = f"{url_alvo}&file={quote(payload)}"  # Usando quote para codificar o payload
    async with httpx.AsyncClient(http2=True) as client:
        resposta_teste = await client.get(url_completa, headers=headers_base)
        
        # Imprime detalhes da resposta para depuração
        #depurar_resposta(resposta_teste, teste_numero, tipo_vulnerabilidade)
        # Usar BeautifulSoup para extrair o título da resposta HTML
        soup = BeautifulSoup(resposta_teste.text, 'html.parser')
        titulo = soup.find('title').string if soup.find('title') else ''

        # Verificar se o teste foi bem-sucedido
        if titulo not in ["Acesso Bloqueado", "Erro"]:
            print(f"Teste #{teste_numero} PASSOU: '{tipo_vulnerabilidade}' - O título é diferente de 'Acesso Bloqueado' ou 'Erro'.")
            return 1
        else:
            print(f"Teste #{teste_numero} FALHOU: '{tipo_vulnerabilidade}' - Título detectado: '{titulo}'.")
            return 0
# Função para imprimir detalhes da resposta para depuração
#def depurar_resposta(resposta, teste_numero, tipo_vulnerabilidade):
    print(f"\nDetalhes da Resposta do Teste #{teste_numero} ({tipo_vulnerabilidade}):")
    print(f"Código de Status: {resposta.status_code}")
    print("Cabeçalhos da Resposta:")
    for chave, valor in resposta.headers.items():
        print(f"  {chave}: {valor}")
    print("Corpo da Resposta (trecho):")
    print(resposta.text[:500])  # Exibe os primeiros 500 caracteres do corpo da resposta para brevidade

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

    # Reportar os resultados finais
    print(f"\nTotal de Testes: {total_testes}")
    print(f"Testes Passaram: {testes_passaram}")
    print(f"Testes Falharam: {testes_falharam}")
    print(f"Url Testada: {url_alvo}") #Depurar e informar a url final que foi alvo

# Executar os testes
if __name__ == "__main__":
    asyncio.run(executar_testes())