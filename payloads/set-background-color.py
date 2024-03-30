import requests
import sys
import os
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

# Construir a URL alvo usando a URL base e o nome da página
url_alvo = f"{url_base}/index.php?page=set-background-color.php"
print(url_alvo)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Lista de campos para testar
campos_formulario = ['background_color']

# Dicionário com payloads para cada tipo de vulnerabilidade, incluindo um para burlar a validação JavaScript
payloads = {
    'XSS': "<script>alert('XSS')</script>",
    'CSS Injection': "background: url(javascript:alert('CSS Injection'));"
}

# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for campo in campos_formulario:
    for tipo_vulnerabilidade, payload in payloads.items():
        # Preparar os dados do formulário, com um campo contendo o payload e os outros 'teste'
        dados_formulario = {c: 'teste' for c in campos_formulario}  # Todos os campos com 'teste'
        dados_formulario[campo] = payload  # Campo atual com o payload

        # Incrementar o contador total de testes
        total_testes += 1

        # Enviar a requisição
        resposta_teste = requests.post(url_alvo, data=dados_formulario, headers=headers)

        print(f"Teste {total_testes}: Campo '{campo}' com payload '{payload}'. Código de status: {resposta_teste.status_code}")

        # Verifica se o teste foi bem-sucedido baseando-se no código de status e no conteúdo da resposta
        if resposta_teste.status_code == 200 and "Acesso Bloqueado" not in resposta_teste.text:
            print(f"Teste #{total_testes} PASSOU: Vulnerabilidade '{tipo_vulnerabilidade}' possivelmente encontrada no campo '{campo}'!")
            testes_passaram += 1
        else:
            print(f"Teste #{total_testes} FALHOU: Código de status: {resposta_teste.status_code} ou acesso bloqueado.")
            testes_falharam += 1
        time.sleep(delay)  # Adiciona uma pausa entre as requisições baseada na taxa de envio
# Reportar os resultados finais
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")
print(f"Url Testada: {url_alvo}")
