
import requests
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Diretório dos logs .json
logs_dir = Path('logs')

if len(sys.argv) > 2:
    url_base = sys.argv[1]  # URL base do DVWA
    taxa_envio = sys.argv[2]  # Taxa de envio (baixo, medio, alto)
else:
    print("URL base e/ou taxa de envio não fornecidas.")
    sys.exit(1)

delays = {'baixo': 7, 'medio': 2, 'alto': 0.5}
delay = delays.get(taxa_envio, 2)  # Padrão é 'medio' se não especificado

url_alvo = f"{{url_base}}DVWA/vulnerabilities/file_upload"

headers = {{
    "User-Agent": "Mozilla/5.0"
}}

payloads = {{
    "payload1": "detalhes do payload",
    "payload2": "detalhes do payload"
}}

total_testes = 0
testes_passaram = 0
testes_falharam = 0

for nome_payload, payload in payloads.items():
    total_testes += 1

    # Modificar a lógica de envio conforme necessário
    resposta_teste = requests.get(url_alvo, headers=headers, params={{'parametro': payload}})

    if resposta_teste.status_code == 200:  # Modificar a lógica de verificação conforme necessário
        print(f"Teste #{{total_testes}} PASSOU: Vulnerabilidade 'File Upload' detectada com payload '{{nome_payload}}'!")
        testes_passaram += 1
    else:
        print(f"Teste #{{total_testes}} FALHOU.")
        testes_falharam += 1

    time.sleep(delay)  # Delay entre os testes

print(f"\nTotal de Testes: {{total_testes}}")
print(f"Testes Passaram: {{testes_passaram}}")
print(f"Testes Falharam: {{testes_falharam}}")
print(f"Url Testada: {{url_alvo}}")

# Gravar resultados
resultados = {{
    'data_hora': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    'url_base': url_base,
    'total_testes': total_testes,
    'testes_passaram': testes_passaram,
    'testes_falharam': testes_falharam,
    'url_testada': url_alvo
}}

nome_arquivo = f"resultados_{{resultados['data_hora']}}.json"
caminho_completo_arquivo = logs_dir / nome_arquivo

with open(caminho_completo_arquivo, 'w') as arquivo:
    json.dump(resultados, arquivo, indent=4)

print(f"Resultados gravados em {{caminho_completo_arquivo}}")
