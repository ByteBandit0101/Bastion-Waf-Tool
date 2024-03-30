import requests
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

url_alvo = f"{url_base}/index.php?page=repeater.php"
print(url_alvo)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def enviar_requisicao_e_verificar_resposta(dados_formulario, tipo_vulnerabilidade, campo, teste_numero):
    resposta_teste = requests.post(url_alvo, data=dados_formulario, headers=headers)
    print(f"Teste {teste_numero}: Campo '{campo}' com payload de '{tipo_vulnerabilidade}'. Código de status: {resposta_teste.status_code}")
    
    if resposta_teste.status_code == 200 and "Acesso Bloqueado" not in resposta_teste.text:
        print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
        return 1
    else:
        print(f"Teste #{teste_numero} FALHOU: Acesso potencialmente bloqueado ou vulnerabilidade não explorada.")
        return 0
    
campos_formulario = ['string_to_repeat', 'times_to_repeat_string']

payloads = {
    'XSS': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'Buffer Overflow': 'A' * 5000  # Ajuste o tamanho conforme necessário
}

total_testes = 0
testes_passaram = 0

for campo in campos_formulario:
    for tipo_vulnerabilidade, payload in payloads.items():
        dados_formulario = {c: 'teste' for c in campos_formulario}
        dados_formulario[campo] = payload

        total_testes += 1
        testes_passaram += enviar_requisicao_e_verificar_resposta(dados_formulario, tipo_vulnerabilidade, campo, total_testes)

dados_formulario = {c: 'teste' for c in campos_formulario}
dados_formulario['parametro_inesperado'] = 'valor_inesperado'
total_testes += 1
testes_passaram += enviar_requisicao_e_verificar_resposta(dados_formulario, 'Parameter Addition', 'parametro_inesperado', total_testes)
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