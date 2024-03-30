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

url_alvo = f"{url_base}/index.php?page=user-info.php"
print(url_alvo)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

campos_formulario = ['username', 'password']

payloads = {
    'SQL Injection': "' OR '1'='1",
    'SQL Injection 2': "admin'#",
    'XSS': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'JavaScript Validation Bypass': "admin' --"
}

total_testes = 0
testes_passaram = 0
testes_falharam = 0

for campo in campos_formulario:
    for tipo_vulnerabilidade, payload in payloads.items():
        dados_formulario = {c: 'teste' for c in campos_formulario}
        dados_formulario[campo] = payload

        total_testes += 1
        resposta_teste = requests.post(url_alvo, data=dados_formulario, headers=headers)

        print(f"Teste {total_testes}: Campo '{campo}' com payload '{payload}'. Código de status: {resposta_teste.status_code}")

        if resposta_teste.status_code == 200 and "Acesso Bloqueado" not in resposta_teste.text:
            print(f"Teste #{total_testes} PASSOU: Vulnerabilidade '{tipo_vulnerabilidade}' possivelmente encontrada no campo '{campo}'!")
            testes_passaram += 1
        else:
            print(f"Teste #{total_testes} FALHOU: Código de status: {resposta_teste.status_code} ou acesso bloqueado.")
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
