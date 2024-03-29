import subprocess
import pathlib

def run_test_script(script_path, url_base, taxa_envio):
    # Comando para executar o script Python externo com a taxa de envio como argumento
    command = ['python', str(script_path), url_base, taxa_envio]
    # Executa o script e captura a saída
    completed_process = subprocess.run(command, text=True, capture_output=True)
    # Retorna a saída padrão do script
    return completed_process.stdout

def main():
    # Solicitar a URL base do usuário
    url_base = input("Por favor, insira a URL base: ")

    # Solicitar a taxa de envio do usuário
    taxa_envio = input("Escolha a taxa de envio de requisições (baixo, medio, alto): ")

    # Caminho para o diretório contendo os scripts de teste
    test_scripts_dir = pathlib.Path('./payloads')  # Atualize este caminho conforme necessário

    # Lista para armazenar os resultados dos testes
    test_results = []

    # Iterando sobre cada script de teste e executando-o
    for test_script in test_scripts_dir.glob('*.py'):
        if test_script.name != 'run_all_tests.py':  # Ignorar o script principal
            print(f'Executando: {test_script.name}')
            # Passa a taxa de envio como argumento para cada script de teste
            result = run_test_script(script_path=test_script, url_base=url_base, taxa_envio=taxa_envio)
            test_results.append((test_script.name, result))

    # Exibindo os resultados
    for script_name, result in test_results:
        print(f'Resultado do {script_name}:\n{result}\n{"-"*60}\n')

if __name__ == '__main__':
    main()