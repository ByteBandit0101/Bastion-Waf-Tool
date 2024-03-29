from bs4 import BeautifulSoup
import sys
import os
import requests

if len(sys.argv) > 1:
    url_base = sys.argv[1]  # Recebe a URL base como argumento do código principal
else:
    print("URL base não foi fornecida.")
    sys.exit(1)

url_alvo = f"{url_base}/index.php?page=dns-lookup.php"
print(url_alvo)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Lista de campos para testar
campos_formulario = ['target_host']

# Dicionário com payloads para cada tipo de vulnerabilidade
payloads = {
    'SQL Injection': "' OR '1'='1",
    'XSS': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'JavaScript Validation Bypass': "admin' --",
    'O/S Command injection': "127.0.0.1 && ls",
    'O/S Command injection': "127.0.0.1;ls -la /",
    'Application Log Injection': "127.0.0.1\nInjected log entry",
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

        # Usar BeautifulSoup para fazer o parsing do HTML da resposta
        soup = BeautifulSoup(resposta_teste.text, 'html.parser')
        titulo = soup.find('title').text if soup.find('title') else ''

        # Print detalhes do teste atual
        print(f"Teste {total_testes}: Campo '{campo}' com payload '{payload}'. Título: {titulo[:46]}")

        # Verificar se o teste foi bem-sucedido
        if titulo != "Acesso Bloqueado":
            print(f"Teste #{total_testes} PASSOU: Vulnerabilidade '{tipo_vulnerabilidade}' encontrada no campo '{campo}'!")
            testes_passaram += 1
        else:
            print(f"Teste #{total_testes} FALHOU: Acesso bloqueado.")
            testes_falharam += 1

# Reportar os resultados finais
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {testes_falharam}")
print(f"Url Testada: {url_alvo}") #Depurar e informar a url final que foi alvo