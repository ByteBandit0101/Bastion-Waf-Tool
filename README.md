<H1>Bastion: A Tool for WAF Evaluation</H1>

Made by <b>ByteBandit</b>

<h1>About the tool</h1>
<p>The WAFHackProbe is designed to automate testing on vulnerable applications, such as OWASP's DVWA (Damn Vulnerable Web Application) and Mutillidae, serves as a benchmarking mechanism for Web Application Firewalls (WAFs). This tool operates by sending a series of carefully crafted payloads known to exploit specific vulnerabilities in these test applications. During these tests, the tool evaluates the applications' responses to each payload sent.</p>

<p>The underlying logic of this tool is straightforward yet effective: it attempts to exploit known vulnerabilities in these applications and monitors how the responses are handled by both the applications and, more crucially, by the WAFs implemented to protect them. When a payload results in a successful exploitation (i.e., the attack "was successful"), it indicates that the WAF failed to block the exploitation attempt, and the tool records this event as a failure in the protection offered by the WAF.</p>

<p>Conversely, if the WAF manages to identify and block the exploitation attempt, preventing the payload from causing any harm or gaining unauthorized access, the tool records this as a success for the WAF ("WAF blocked it"). This continuous testing process allows for a comparative assessment of the effectiveness of different WAFs in protecting against a standardized set of known attacks.</p>

<p>This automated approach not only saves significant time that would otherwise be spent on manual testing but also provides a quantitative metric on the effectiveness of WAFs in protecting web applications against known exploitation attempts. This tool can be extremely useful for organizations looking to strengthen their cyber defenses by evaluating different WAF solutions before making a large-scale implementation.</p>
  <section>
  <h1>Exploited vulnerabilities</h1>
  <h1>Multilidae</h1>      
  <h2>add-to-your-blog.php</h2>
        <ul>
            <li>SQL Injection on blog entry</li>
            <li>SQL Injection on logged in user name</li>
            <li>Cross site scripting on blog entry</li>
            <li>Cross site scripting on logged in user name</li>
            <li>Log injection on logged in user name</li>
            <li>Cross site request forgery</li>
            <li>JavaScript validation bypass</li>
            <li>XSS in the form title via logged in username</li>
            <li>HTML injection in blog input field</li>
            <li>Application Exception Output</li>
            <li>Application Log Injection</li>
            <li>Known Vulnerable Output: Name Comment "Add blog for" title</li>
        </ul>
    </section>

   <section>
        <h2>arbitrary-file-inclusion.php</h2>
        <ul>
            <li>System file compromise</li>
            <li>Load any page from any site</li>
            <li>Reflected XSS via the value in the "page" URL parameter</li>
            <li>Server-side includes</li>
            <li>HTML injection</li>
            <li>Remote File Inclusion</li>
            <li>Local File Inclusion</li>
            <li>Method Tampering</li>
        </ul>
    </section>
     <section>
        <h2>back-button-discussion.php</h2>
        <ul>
            <li>Reflected XSS via referer HTTP header</li>
            <li>JS Injection via referer HTTP header</li>
            <li>HTML injection via referer HTTP header</li>
            <li>Unvalidated redirect</li>
        </ul>
    </section>

   
  <section>
        <h2>browser-info.php</h2>
        <ul>
            <li>Reflected XSS via referer HTTP header</li>
            <li>JS Injection via referer HTTP header</li>
            <li>HTML injection</li>
            <li>Reflected XSS via user-agent string HTTP header</li>
        </ul>
  </section>

    
  <section>
        <h2>dns-lookup.php</h2>
        <ul>
            <li>Cross site scripting on the host/ip field</li>
            <li>O/S Command injection on the host/ip field</li>
            <li>This page writes to the log. SQLi and XSS on the log are possible</li>
            <li>HTML injection</li>
            <li>GET for POST (method tampering) is possible</li>
            <li>Application Log Injection</li>
            <li>JavaScript Validation Bypass</li>
        </ul>
  </section>

   
  <section>
        <h2>document-viewer.php</h2>
        <ul>
            <li>Cross Site Scripting</li>
            <li>HTML injection</li>
            <li>HTTP Parameter Pollution</li>
            <li>Frame source injection</li>
            <li>Method Tampering</li>
            <li>Application Log Injection</li>
        </ul>
  </section>

   
  <section>
        <h2>login.php</h2>
        <ul>
            <li>Authentication bypass SQL injection via username and password fields</li>
            <li>SQL injection via username and password fields</li>
            <li>XSS via username field</li>
            <li>JavaScript validation bypass</li>
            <li>HTML injection via username field</li>
            <li>Username enumeration</li>
            <li>Application Log Injection</li>
        </ul>
  </section>
  <section>
        <h2>register.php</h2>
        <ul>
            <li>SQL injection, HTML injection, and XSS via username, signature, and password fields</li>
            <li>Method tampering</li>
            <li>Application Log Injection</li>
        </ul>
    </section>

    
  <section>
        <h2>repeater.php</h2>
        <ul>
            <li>HTML injection and XSS</li>
            <li>Method tampering</li>
            <li>Parameter addition</li>
            <li>Buffer overflow</li>
        </ul>
  </section>

  
  <section>
        <h2>set-background-color.php</h2>
        <ul>
            <li>Cascading style sheet injection and XSS via the color field</li>
        </ul>
  </section>

   
  <section>
        <h2>user-info.php</h2>
        <ul>
            <li>SQL injection to dump all usernames and passwords via username or password field</li>
            <li>XSS via any of the displayed fields</li>
            <li>XSS via the username field</li>
            <li>JavaScript validation bypass</li>
        </ul>
  </section>

    
  <section>
        <h2>user-poll.php</h2>
        <ul>
            <li>Parameter pollution</li>
            <li>Method Tampering</li>
            <li>XSS via the choice parameter</li>
            <li>Cross site request forgery to force user choice</li>
            <li>HTML injection</li>
        </ul>
  </section>

   
  <section>
        <h2>xml-validator.php</h2>
        <ul>
            <li>XML Entity Injection Attack</li>
            <li>XML Entity Expansion</li>
            <li>XML Injection</li>
            <li>Reflected Cross site scripting via XML Injection</li>
        </ul>

  <h1>DVWA</h1> 
  <h2>Brute Force</h2>
    <ul></ul>

  <h2>Command Injection</h2>
    <ul></ul>

  <h2>CSRF</h2>
    <ul></ul>

  <h2> File Inclusion</h2>
    <ul></ul>

  <h2>  File Upload</h2>
    <ul></ul>

  <h2>Insecure CAPTCHA </h2>
    <ul></ul>

  <h2>SQL Injection</h2>
    <ul></ul>

  <h2>SQL Injection (Blind)</h2>
    <ul></ul>
  
  <h2>Weak Session IDs</h2>
    <ul></ul>

  <h2>XSS (DOM)</h2>
    <ul></ul>
  
  <h2>XSS (Reflect)</h2>
    <ul></ul>

  <h2>XSS (Stored)</h2>
    <ul></ul>

  <h2>CSP Bypass</h2>
    <ul></ul>

  <h2>JavaScript</h2>
    <ul></ul>

  <h2>Authorisation Bypass</h2>
    <ul></ul>

  <h2>Open HTTP Redirect</h2>
    <ul></ul>
    
  </section>
