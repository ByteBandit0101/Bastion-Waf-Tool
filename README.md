<H1>Waf Benchmark</H1>
Made by <b>ByteBandit</b>

<h1>Resumo da exploração</h1>
<p>Basicamente a ferramenta irá executar scripts com payloads que exploram as vulnerabilidades existentes em páginas vulberaveis de aplicações de testes> DVWA e multilidae:</p>
  <section>
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
