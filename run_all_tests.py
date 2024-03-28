import importlib.util
import pathlib
import sys
from io import StringIO

def run_test_script(script_path):
    # Capturar a saída padrão
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    # Carregar e executar o módulo do script de teste
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    # Capturar a saída do script
    result = sys.stdout.getvalue()

    # Restaurar a saída padrão
    sys.stdout = original_stdout

    return result

def main():
    # Caminho para o diretório contendo os scripts de teste
    test_scripts_dir = pathlib.Path('./payloads')  # Assume que os scripts estão no diretório atual

    # Lista para armazenar os resultados dos testes
    test_results = []

    # Iterando sobre cada script de teste e executando-o
    for test_script in test_scripts_dir.glob('*.py'):
        if test_script.name != 'run_all_tests.py':  # Ignorar o script principal
            print(f'Executando: {test_script.name}')
            result = run_test_script(test_script)
            test_results.append((test_script.name, result))

    # Exibindo os resultados
    for script_name, result in test_results:
        print(f'Resultado do {script_name}:\n{result}\n{"-"*60}\n')

if __name__ == '__main__':
    main()