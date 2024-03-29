import requests
from bs4 import BeautifulSoup
import sys
import os

if len(sys.argv) > 1:
    url_base = sys.argv[1]  # Recebe a URL base como argumento do código principal
else:
    print("URL base não foi fornecida.")
    sys.exit(1)

# Obter o nome do arquivo do script atual e remover a extensão '.py' para obter o nome da página
script_name = os.path.basename(__file__).replace('.py', '')

# Construir a URL alvo usando a URL base e o nome da página
url_alvo = f"{url_base}/index.php?page={script_name}.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Lista de campos para testar
campos_formulario = ['blog_entry', 'logged_in_user_name']

# Dicionário com payloads para cada tipo de vulnerabilidade
payloads = {
    'SQL Injection': "' OR '1'='1",
    'XSS': "<script>alert('XSS')</script>",
    # Adicione outros payloads conforme necessário
}

# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for campo in campos_formulario:
    for tipo_vulnerabilidade, payload in payloads.items():
        dados_formulario = {c: 'teste' for c in campos_formulario}  # Todos os campos com 'teste'
        dados_formulario[campo] = payload  # Campo atual com o payload

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
print(url_alvo)
