import importlib.util
import pathlib
import sys
from io import StringIO

def run_test_script(script_path, url_base):
    # Configurando o ambiente do script com a URL base
    original_argv = sys.argv  # Corrigido aqui
    sys.argv = [str(script_path), url_base]  # Simula argumentos de linha de comando para o script, incluindo a URL base

    # Capturar a saída padrão
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    # Carregar e executar o módulo do script de teste
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    # Capturar a saída do script
    result = sys.stdout.getvalue()

    # Restaurar a saída padrão e os argumentos originais
    sys.stdout = original_stdout
    sys.argv = original_argv  # Restaura os argumentos originais

    return result

def main():
    # Solicitar a URL base do usuário
    url_base = input("Por favor, insira a URL base: ")

    # Caminho para o diretório contendo os scripts de teste
    test_scripts_dir = pathlib.Path('.')  # Atualize este caminho conforme necessário

    # Lista para armazenar os resultados dos testes
    test_results = []

    # Iterando sobre cada script de teste e executando-o
    for test_script in test_scripts_dir.glob('*.py'):
        if test_script.name != 'run_all_tests.py':  # Ignorar o script principal
            print(f'Executando: {test_script.name}')
            result = run_test_script(script_path=test_script, url_base=url_base)
            test_results.append((test_script.name, result))

    # Exibindo os resultados
    for script_name, result in test_results:
        print(f'Resultado do {script_name}:\n{result}\n{"-"*60}\n')

if __name__ == '__main__':
    main()
