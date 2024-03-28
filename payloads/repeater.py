import requests
from bs4 import BeautifulSoup

# Configurações iniciais
url_alvo = "https://sone.codatahml.pb.gov.br/index.php?page=repeater.php"  # Alterado para user-info.php
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Função para enviar a requisição e verificar a resposta
def enviar_requisicao_e_verificar_resposta(dados_formulario, tipo_vulnerabilidade, campo, teste_numero):
    resposta_teste = requests.post(url_alvo, data=dados_formulario, headers=headers)
    soup = BeautifulSoup(resposta_teste.text, 'html.parser')
    titulo = soup.find('title').text if soup.find('title') else ''
    print(f"Teste {teste_numero}: Campo '{campo}' com payload de '{tipo_vulnerabilidade}'. Título: {titulo[:46]}")
    
    if titulo != "Acesso Bloqueado":
        print(f"Teste #{teste_numero} PASSOU: Vulnerabilidade de '{tipo_vulnerabilidade}' possivelmente encontrada!")
        return 1
    else:
        print(f"Teste #{teste_numero} FALHOU: Acesso bloqueado.")
        return 0

# Lista de campos para testar
campos_formulario = ['string_to_repeat', 'times_to_repeat_string']

# Dicionário com payloads para vulnerabilidades específicas
payloads = {
    'XSS': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'Buffer Overflow': 'A' * 5000  # Ajuste o tamanho conforme necessário
}

# Contadores para os resultados dos testes
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# Realizar os testes
for campo in campos_formulario:
    # Testando vulnerabilidades específicas em cada campo
    for tipo_vulnerabilidade, payload in payloads.items():
        dados_formulario = {c: 'teste' for c in campos_formulario}
        dados_formulario[campo] = payload  # Substitui o valor de um campo pelo payload

        # Enviar a requisição e verificar a resposta
        total_testes += 1
        testes_passaram += enviar_requisicao_e_verificar_resposta(dados_formulario, tipo_vulnerabilidade, campo, total_testes)

# Teste de Parameter Addition
dados_formulario = {c: 'teste' for c in campos_formulario}
dados_formulario['parametro_inesperado'] = 'valor_inesperado'  # Adiciona um parâmetro inesperado
total_testes += 1
testes_passaram += enviar_requisicao_e_verificar_resposta(dados_formulario, 'Parameter Addition', 'parametro_inesperado', total_testes)

# Reportar os resultados finais
print(f"\nTotal de Testes: {total_testes}")
print(f"Testes Passaram: {testes_passaram}")
print(f"Testes Falharam: {total_testes - testes_passaram}")