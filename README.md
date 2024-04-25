<a name="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]




<H1>BASTION: A Tool for WAF Evaluation</H1>
<p align="center">
<img src=https://github.com/ByteBandit0101/Bastion-Waf-Tool/assets/111284802/c8faa530-b8fe-45d8-ae86-93a3a46131c1></p>
<p align="center">Made by <b>ByteBandit0101</b></p>
<p align="center">
<img src=http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge></p>

<p align="center"><b>⚠️WARNING⚠️</b></p>
<p align="center">This tool is intended for testing in controlled environments with the intent of evaluating wafs</p>


<h1>About the tool</h1>
<p>The Bastion is designed to automate testing on vulnerable applications, such as OWASP's DVWA (Damn Vulnerable Web Application) and Mutillidae, serves as a benchmarking mechanism for Web Application Firewalls (WAFs). This tool operates by sending a series of carefully crafted payloads known to exploit specific vulnerabilities in these test applications. During these tests, the tool evaluates the applications' responses to each payload sent.</p>

<p>The underlying logic of this tool is straightforward yet effective: it attempts to exploit known vulnerabilities in these applications and monitors how the responses are handled by both the applications and, more crucially, by the WAFs implemented to protect them. When a payload results in a successful exploitation (i.e., the attack "was successful"), it indicates that the WAF failed to block the exploitation attempt, and the tool records this event as a failure in the protection offered by the WAF.</p>

<p>Conversely, if the WAF manages to identify and block the exploitation attempt, preventing the payload from causing any harm or gaining unauthorized access, the tool records this as a success for the WAF ("WAF blocked it"). This continuous testing process allows for a comparative assessment of the effectiveness of different WAFs in protecting against a standardized set of known attacks.</p>

<p>This automated approach not only saves significant time that would otherwise be spent on manual testing but also provides a quantitative metric on the effectiveness of WAFs in protecting web applications against known exploitation attempts. This tool can be extremely useful for organizations looking to strengthen their cyber defenses by evaluating different WAF solutions before making a large-scale implementation.</p>

### Built With
[![python][Python.py]][Python-url]


### Installation

## Linux
1. Clone the repo
   ```sh
   git clone https://github.com/ByteBandit0101/Bastion-Waf-Tool.git
   ```
2. Go to Bastion-Waf-Tool directory
   ```sh
   cd Bastion-Waf-Tool
   ```
3. Install requeriments.txt
   ```js
   pip install requeriments.txt
   ```
4. Run
   ```js
   python3 run_all_tests.py
   ```
## Windows
1. Clone the repo
   ```sh
   git clone https://github.com/ByteBandit0101/Bastion-Waf-Tool.git
   ```
2. Go to Bastion-Waf-Tool directory
   ```sh
   cd Bastion-Waf-Tool
   ```
3. Install requeriments.txt
   ```js
   pip install requeriments.txt
   ```
4. Run
   ```js
   python run_all_tests.py
   ```
### How To Use
1. Choose the scenario
   ```sh
   1. Explore Mutillidae
   2. Explore DVWA
   3. Exit
   Choose an option: "Enter the desired option"
   ```
2. Enter the target url
   (Example: https://test.com)
   ```sh
   Please enter the base URL: "put your url here"
   ```
3. Select the speed of requests:
   low = 10 / medium = 5 / high = 3
   ```sh
   Choose the request send rate (low, medium, high):"Enter the desired option"
   ```
4. Choose whether you want to run all tests or choose which ones will be run:
   ```sh
   Do you want to run all tests automatically or select them manually?
   1. Run all tests automatically
   2. Select tests manually
   Choose an option: "put your url here"
   ```
   #### Case 1:
   It will run all the scripts in order and at the end give an overview of the test results
   ```sh
   Do you want to run all tests automatically or select them manually?
   1. Run all tests automatically
   2. Select tests manually
   Choose an option: 1
   ```

   #### Case 2:
   If you choose <b>"yes"</b> it will run the script that is defined, and at the end it will ask if you want to run the next ones.
   ```sh
   Choose an option: 2
   Do you want to execute Brute_Force.py? (yes/no): yes
   ```
   If you choose <b>"no" </b>it will ignore the current script and skip to the next one asking if you want to run it.
   ```sh
   Choose an option: 2
   Do you want to execute Brute_Force.py? (yes/no): no
   ```

      
6. At the end of the test you can choose to save the logs in a .zip (save) or delete them (clear):
   ```sh
   Do you want to clear the logs folder or save? (clear/save): "Enter the desired option"
   ```
  ### Exploited vulnerabilities
  Here are the pages that BASTION exploits in both Multilidae and DVWA and their respective vulnerabilities
  <h3>Multilidae</h3>      
  <h3>add-to-your-blog.php</h3>
        <ul>
            <ul>SQL Injection on blog entry</ul>
            <ul>SQL Injection on logged in user name</ul>
            <ul>Cross site scripting on blog entry</ul>
            <ul>Cross site scripting on logged in user name</ul>
            <ul>Log injection on logged in user name</ul>
            <ul>Cross site request forgery</ul>
            <ul>JavaScript validation bypass</ul>
            <ul>XSS in the form title via logged in username</ul>
            <ul>HTML injection in blog input field</ul>
            <ul>Application Exception Output</ul>
            <ul>Application Log Injection</ul>
            <ul>Known Vulnerable Output: Name Comment "Add blog for" title</ul>
        </ul>
    </section>

   <section>
        <h3>arbitrary-file-inclusion.php</h3>
        <ul>
            <ul>System file compromise</ul>
            <ul>Load any page from any site</ul>
            <ul>Reflected XSS via the value in the "page" URL parameter</ul>
            <ul>Server-side includes</ul>
            <ul>HTML injection</ul>
            <ul>Remote File Inclusion</ul>
            <ul>Local File Inclusion</ul>
            <ul>Method Tampering</ul>
        </ul>
    </section>
     <section>
        <h3>back-button-discussion.php</h3>
        <ul>
            <ul>Reflected XSS via referer HTTP header</ul>
            <ul>JS Injection via referer HTTP header</ul>
            <ul>HTML injection via referer HTTP header</ul>
            <ul>Unvalidated redirect</ul>
        </ul>
    </section>

   
  <section>
        <h3>browser-info.php</h3>
        <ul>
            <ul>Reflected XSS via referer HTTP header</ul>
            <ul>JS Injection via referer HTTP header</ul>
            <ul>HTML injection</ul>
            <ul>Reflected XSS via user-agent string HTTP header</ul>
        </ul>
  </section>

    
  <section>
        <h3>dns-lookup.php</h3>
        <ul>
            <ul>Cross site scripting on the host/ip field</ul>
            <ul>O/S Command injection on the host/ip field</ul>
            <ul>This page writes to the log. SQLi and XSS on the log are possible</ul>
            <ul>HTML injection</ul>
            <ul>GET for POST (method tampering) is possible</ul>
            <ul>Application Log Injection</ul>
            <ul>JavaScript Validation Bypass</ul>
        </ul>
  </section>

   
  <section>
        <h3>document-viewer.php</h3>
        <ul>
            <ul>Cross Site Scripting</ul>
            <ul>HTML injection</ul>
            <ul>HTTP Parameter Pollution</ul>
            <ul>Frame source injection</ul>
            <ul>Method Tampering</ul>
            <ul>Application Log Injection</ul>
        </ul>
  </section>

   
  <section>
        <h3>login.php</h3>
        <ul>
            <ul>Authentication bypass SQL injection via username and password fields</ul>
            <ul>SQL injection via username and password fields</ul>
            <ul>XSS via username field</ul>
            <ul>JavaScript validation bypass</ul>
            <ul>HTML injection via username field</ul>
            <ul>Username enumeration</ul>
            <ul>Application Log Injection</ul>
        </ul>
  </section>
  <section>
        <h3>register.php</h3>
        <ul>
            <ul>SQL injection, HTML injection, and XSS via username, signature, and password fields</ul>
            <ul>Method tampering</ul>
            <ul>Application Log Injection</ul>
        </ul>
    </section>

    
  <section>
        <h3>repeater.php</h3>
        <ul>
            <ul>HTML injection and XSS</ul>
            <ul>Method tampering</ul>
            <ul>Parameter addition</ul>
            <ul>Buffer overflow</ul>
        </ul>
  </section>

  
  <section>
        <h3>set-background-color.php</h3>
        <ul>
            <ul>Cascading style sheet injection and XSS via the color field</ul>
        </ul>
  </section>

   
  <section>
        <h3>user-info.php</h3>
        <ul>
            <ul>SQL injection to dump all usernames and passwords via username or password field</ul>
            <ul>XSS via any of the displayed fields</ul>
            <ul>XSS via the username field</ul>
            <ul>JavaScript validation bypass</ul>
        </ul>
  </section>

    
  <section>
        <h3>user-poll.php</h3>
        <ul>
            <ul>Parameter pollution</ul>
            <ul>Method Tampering</ul>
            <ul>XSS via the choice parameter</ul>
            <ul>Cross site request forgery to force user choice</ul>
            <ul>HTML injection</ul>
        </ul>
  </section>

   
  <section>
        <h3>xml-validator.php</h3>
         <ul>
           <ul>XML Entity Injection Attack </ul>
           <ul>XML Entity Expansion </ul>
           <ul>XML Injection </ul>
           <ul>Reflected Cross site scripting via XML Injection </ul>
         </ul>
       

  <h3>DVWA - Damn Vulnerable Web Application</h3> 
  <h3>Brute Force</h3>
    <ul>This vulnerability allows an attacker to try many passwords or keys with the hope of eventually guessing correctly. DVWA can be used to practice brute force attacks on login forms.</ul>

  <h3>Command Injection</h3>
    <ul>This security flaw occurs when an attacker can inject arbitrary commands into an operating system through a vulnerable application, typically through web forms.</ul>

  <h3>CSRF</h3>
    <ul>A CSRF attack tricks a user's browser into performing unwanted actions on a site where they are currently authenticated, exploiting the trust that a site has in the user's browser.</ul>

  <h3> File Inclusion</h3>
    <ul> There are two types of file inclusion: Local File Inclusion (LFI) and Remote File Inclusion (RFI). These vulnerabilities allow an attacker to include files on the server or via remote URLs, respectively, which can lead to arbitrary code execution. </ul>

  <h3>  File Upload</h3>
    <ul>This vulnerability occurs when an application allows users to upload files without proper security checks, enabling the upload of malicious scripts that can be executed on the server.</ul>

  <h3>Insecure CAPTCHA </h3>
    <ul>CAPTCHAs are used to ensure that the user is human and not a bot. An insecure CAPTCHA can be automated or bypassed, allowing bots to perform malicious actions.</ul>

  <h3>SQL Injection</h3>
    <ul>This is one of the most dangerous vulnerabilities, where an attacker can inject arbitrary SQL commands, which are executed by the database. This can lead to the exposure of sensitive data, data corruption, or loss of control over the database.</ul>

  <h3>SQL Injection (Blind)</h3>
    <ul> A variation of SQL Injection where the attacker cannot see the result of the injection directly, but can infer information through the application's behavior or through indirect error messages.</ul>
  
  <h3>Weak Session IDs</h3>
    <ul>Weak session IDs can be easily guessed or predicted, allowing an attacker to hijack another user's session, thereby taking control over someone else's account.</ul>

  <h3>XSS (DOM, Reflect, Stored)</h3>
    <ul>Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into pages viewed by other users. Stored XSS stores the malicious script on the server; Reflected XSS sends the script as part of a request that is reflected by the server to the user; DOM XSS manipulates the DOM to inject the malicious script.</ul>

  <h3>CSP Bypass</h3>
    <ul>Content Security Policy (CSP) is a security measure to detect and mitigate attacks such as XSS and data injection. A CSP bypass allows the attacker to circumvent CSP restrictions, executing unauthorized scripts.</ul>

  <h3>JavaScript</h3>
    <ul>Vulnerabilities in JavaScript can include security issues in how JavaScript code is executed or manipulated, allowing various attacks, including XSS.</ul>

  <h3>Authorisation Bypass</h3>
    <ul>This vulnerability occurs when authorization restrictions in an application are poorly configured or can be circumvented, allowing a user to access functions or data without the necessary permissions.</ul>

  <h3>Open HTTP Redirect</h3>
    <ul>This vulnerability happens when a web application redirects users to other URLs using untrusted input data, which can lead to phishing attacks or other misuses.</ul>
    
  </section>

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/lucazeved/
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://https://github.com/ByteBandit0101/Bastion-Waf-Tool/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/ByteBandit0101/Bastion-Waf-Tool/issues
[Python.py]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/


