import requests
import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# JSON log directory
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)  # Script to create log folder when it does not exist

if len(sys.argv) > 2:
    base_url = sys.argv[1]  # Receives the base URL as the main code argument
    send_rate = sys.argv[2]  # Receives the send rate as the second argument
else:
    print("Base URL and/or send rate not provided.")
    sys.exit(1)

# Maps the send rate to a specific time interval
delays = {'low': 7, 'medium': 2, 'high': 0.5}
delay = delays.get(send_rate, 2)  # Uses 'medium' as default if the rate is not recognized

target_url = f"{base_url}/index.php?page=set-background-color.php"
print(target_url)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# List of fields to test
form_fields = ['background_color']

# Dictionary with payloads for each type of vulnerability, including one to bypass JavaScript validation
payloads = {
    'XSS': "<script>alert('XSS')</script>",
    'CSS Injection': "background: url(javascript:alert('CSS Injection'));"
}

# Counters for test results
total_tests = 0
tests_passed = 0
tests_failed = 0

# Conducting tests
for field in form_fields:
    for vulnerability_type, payload in payloads.items():
        # Prepare form data, with one field containing the payload and the others 'test'
        form_data = {c: 'test' for c in form_fields}  # All fields with 'test'
        form_data[field] = payload  # Current field with the payload

        # Increment the total test counter
        total_tests += 1

        # Send the request
        test_response = requests.post(target_url, data=form_data, headers=headers)

        print(f"Test {total_tests}: Field '{field}' with payload '{payload}'. Status code: {test_response.status_code}")

        # Check if the test was successful based on the status code and response content
        if test_response.status_code == 200 and "Access Blocked" not in test_response.text:
            print(f"Test #{total_tests} PASSED: Vulnerability '{vulnerability_type}' potentially found in field '{field}'!")
            tests_passed += 1
        else:
            print(f"Test #{total_tests} FAILED: Status code: {test_response.status_code} or blocked access.")
            tests_failed += 1
        time.sleep(delay)  # Adds a pause between requests based on the send rate

# Reporting final results
print(f"\nTotal Tests: {total_tests}")
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {tests_failed}")
print(f"Tested URL: {target_url}")

# Data retrieval part
# Record the results in a JSON file
results = {
    'date_time': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    'base_url': base_url,
    'total_tests': total_tests,
    'tests_passed': tests_passed,
    'tests_failed': tests_failed,
    'tested_url': target_url
}

file_name = f"results_{results['date_time']}.json"
full_file_path = logs_dir.joinpath(file_name)

with open(full_file_path, 'w') as file:
    json.dump(results, file, indent=4)

print(f"\nResults recorded in {full_file_path}")