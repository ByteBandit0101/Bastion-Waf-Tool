import subprocess
import pathlib
import sys
import json
from pathlib import Path
import shutil  # Import necessário para remover diretórios

logs_dir = Path('./logs')# diretório para fazer merge dos logs

def run_test_script(script_path, url_base, taxa_envio):
    # Comando para executar o script Python externo com a taxa de envio como argumento
    command = ['python', str(script_path), url_base, taxa_envio]
    # Executa o script e captura a saída
    completed_process = subprocess.run(command, text=True, capture_output=True)
    # Retorna a saída padrão do script
    return completed_process.stdout
def display_welcome_message():
    ascii_art = """
     ____        _       ____                  _   _   
    |  _ \      | |     |  _ \                | (_) |  
    | |_) |_   _| |_ ___| |_) | __ _ _ __   __| |_| |_ 
    |  _ <| | | | __/ _ \  _ < / _` | '_ \ / _` | | __|
    | |_) | |_| | |_  __/ |_) | (_| | | | | (_| | | |_ 
    |____/ \__, |\__\___|____/ \__,_|_| |_|\__,_|_|\__|
            __/ |                       Made by               
           |___/                                       
    """  
    print(ascii_art)
    print("Bem-vindo ao WAFHackProbe!\n")
    print("1. Explorar Multilidae")
    print("2. Explorar DVWA")
    print("3. Sair")
    choice = input("Escolha uma opção: ")
    return choice

#Função para limpar as pastas logs se quiser..
def limpar_pasta_logs():
    try:
        # Confirmação do usuário para limpar a pasta 'logs'
        escolha_limpar = input("\nDeseja limpar a pasta de logs? (s/n): ").lower()
        if escolha_limpar == 's':
            shutil.rmtree(logs_dir)
            print("Pasta de logs limpa com sucesso.")
            logs_dir.mkdir()  # Recria a pasta 'logs' após a limpeza
        elif escolha_limpar == 'n':
            print("A pasta de logs não foi limpa.")
        else:
            print("Opção inválida. A pasta de logs não foi limpa.")
    except Exception as e:
        print(f"Erro ao limpar a pasta de logs: {e}")
        
def main():
    choice = display_welcome_message()
    if choice == '1':
        # Solicitar a URL base do usuário
        url_base = input("Por favor, insira a URL base: ")
        # Solicitar a taxa de envio do usuário
        taxa_envio = input("Escolha a taxa de envio de requisições (baixo, medio, alto): ")
        # Caminho para o diretório contendo os scripts de teste
        test_scripts_dir = pathlib.Path('./payloads_Multilidae')  # Atualize este caminho conforme necessário

        # Lista para armazenar os resultados dos testes
        test_results = []
        
        # Variáveis para armazenar os totais agregados
        total_testes_agregados = 0
        testes_passaram_agregados = 0
        testes_falharam_agregados = 0

        # Iterando sobre cada script de teste e executando-o
        for test_script in test_scripts_dir.glob('*.py'):
            if test_script.name != 'run_all_tests.py':  # Ignorar o script principal
                print(f'Executando: {test_script.name}')
                # Passa a taxa de envio como argumento para cada script de teste
                result = run_test_script(script_path=test_script, url_base=url_base, taxa_envio=taxa_envio)
                test_results.append((test_script.name, result))

        # Exibindo os resultados unicos
        for script_name, result in test_results:
            print(f'Resultado do {script_name}:\n{result}\n{"-"*60}\n')
            
        
        # Use um padrão mais geral para encontrar todos os arquivos de resultados
        padrao_nome_arquivo = 'resultados_*.json'

        # Ler e resumir os resultados de todos os arquivos JSON gerados
        for arquivo_resultado in logs_dir.glob(padrao_nome_arquivo):
            with open(arquivo_resultado, 'r') as arquivo:
                resultado = json.load(arquivo)
                total_testes_agregados += resultado['total_testes']
                testes_passaram_agregados += resultado['testes_passaram']
                testes_falharam_agregados += resultado['testes_falharam']

        # Imprimir os totais agregados
        print(f'\nResultados Agregados de Todos os Scripts:')
        print(f'Total de Testes: {total_testes_agregados}')
        print(f'Testes Passaram: {testes_passaram_agregados}')
        print(f'Testes Falharam: {testes_falharam_agregados}')
        
    elif choice == '2':
         # Solicitar a URL base do usuário
        url_base = input("Por favor, insira a URL base: ")
        # Solicitar a taxa de envio do usuário
        taxa_envio = input("Escolha a taxa de envio de requisições (baixo, medio, alto): ")
        # Caminho para o diretório contendo os scripts de teste
        test_scripts_dir = pathlib.Path('./payloads_DVWA')  # Atualize este caminho conforme necessário

        # Lista para armazenar os resultados dos testes
        test_results = []
        
        # Variáveis para armazenar os totais agregados
        total_testes_agregados = 0
        testes_passaram_agregados = 0
        testes_falharam_agregados = 0

        # Iterando sobre cada script de teste e executando-o
        for test_script in test_scripts_dir.glob('*.py'):
            if test_script.name != 'run_all_tests.py':  # Ignorar o script principal
                print(f'Executando: {test_script.name}')
                # Passa a taxa de envio como argumento para cada script de teste
                result = run_test_script(script_path=test_script, url_base=url_base, taxa_envio=taxa_envio)
                test_results.append((test_script.name, result))

        # Exibindo os resultados unicos
        for script_name, result in test_results:
            print(f'Resultado do {script_name}:\n{result}\n{"-"*60}\n')
        
        # Ler e resumir os resultados de todos os arquivos JSON gerados
        padrao_nome_arquivo = f'resultados_{test_script.stem}_*.json'
        for arquivo_resultado in logs_dir.glob(padrao_nome_arquivo):
            with open(arquivo_resultado, 'r') as arquivo:
                resultado = json.load(arquivo)
                total_testes_agregados += resultado['total_testes']
                testes_passaram_agregados += resultado['testes_passaram']
                testes_falharam_agregados += resultado['testes_falharam']
                
        # Após processar todos os arquivos, imprimir os totais agregados
        print(f'\nResultados Agregados de Todos os Scripts:')
        print(f'Total de Testes: {total_testes_agregados}')
        print(f'Testes Passaram: {testes_passaram_agregados}')
        print(f'Testes Falharam: {testes_falharam_agregados}')
        
    elif choice == '3':
        print("Saindo do WaFBenchMulti. Até mais!")
        sys.exit(0)
    else:
        print("Opção inválida. Saindo...")
        sys.exit(1)

if __name__ == '__main__':
    main()
    # Função para perguntar ao usuário sobre a limpeza da pasta 'logs'
    limpar_pasta_logs()