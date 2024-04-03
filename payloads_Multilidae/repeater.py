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

target_url = f"{base_url}/index.php?page=repeater.php"
print(target_url)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def send_request_and_check_response(form_data, vulnerability_type, field, test_number):
    test_response = requests.post(target_url, data=form_data, headers=headers)
    print(f"Test {test_number}: Field '{field}' with payload '{vulnerability_type}'. Status code: {test_response.status_code}")
    
    if test_response.status_code == 200 and "Access Blocked" not in test_response.text:
        print(f"Test #{test_number} PASSED: Potential vulnerability '{vulnerability_type}' found!")
        return 1
    else:
        print(f"Test #{test_number} FAILED: Potential access blocked or vulnerability not exploited.")
        return 0
    
form_fields = ['string_to_repeat', 'times_to_repeat_string']

payloads = {
    'XSS': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'Buffer Overflow': 'A' * 5000  # Adjust size as needed
}

total_tests = 0
tests_passed = 0

for field in form_fields:
    for vulnerability_type, payload in payloads.items():
        form_data = {c: 'test' for c in form_fields}
        form_data[field] = payload

        total_tests += 1
        tests_passed += send_request_and_check_response(form_data, vulnerability_type, field, total_tests)

form_data = {c: 'test' for c in form_fields}
form_data['unexpected_parameter'] = 'unexpected_value'
total_tests += 1
tests_passed += send_request_and_check_response(form_data, 'Parameter Addition', 'unexpected_parameter', total_tests)

time.sleep(delay)  # Adds a pause between requests based on the send rate

print(f"\nTotal Tests: {total_tests}")
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {total_tests - tests_passed}")
print(f"Tested URL: {target_url}")

# Data retrieval part
# Record the results in a JSON file
results = {
    'date_time': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    'base_url': base_url,
    'total_tests': total_tests,
    'tests_passed': tests_passed,
    'tests_failed': total_tests - tests_passed,
    'tested_url': target_url
}

file_name = f"results_{results['date_time']}.json"
full_file_path = logs_dir.joinpath(file_name)

with open(full_file_path, 'w') as file:
    json.dump(results, file, indent=4)

print(f"\nResults recorded in {full_file_path}")