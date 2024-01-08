# OBJECTIVE 4 - Reportinator #

## OBJECTIVE : ##
>Noel Boetie used ChatGPT to write a pentest report.  Go to Christmas Island and help him clean it up.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 4</summary>
  
>-	I know AI sometimes can get specifics wrong unless the prompts are well written. Maybe chatNPT made some mistakes here.
</details>

#  

## PROCEDURE : ##

Reading through the report *carefully* I can spot a number of issues with the reported findings:

### 3. Remote Code Execution via Java Deserialization of Stored Database Objects ###
-	TCP port 88555 is not a valid port number
-	NIST SP 800-53 SC-28 applies to data at rest which is not the case here.

### 6. Stored Cross-Site Scripting Vulnerabilities ###
-	there is no such thing as a HTTP SEND method
-	there is no such thing as “XSS attack language”
-	Listing 5 appears to be an incorrect way of testing for XSS – a better way to test would be to try passing something like: `<script>alert(1)</script>`

### 9. Internal IP Address disclosure: ###
-	there is no such thing as a HTTP 7.4.33 request
-	the recommendation states that the HTTP ‘location’ header should be modified to reflect the host Windows registration key – this is of course not a good idea.  Instead, it should give the relative path to a redirect page.
 
