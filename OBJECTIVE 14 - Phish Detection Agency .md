# OBJECTIVE 14 - Phish Detection Agency #
_Completed by 8.01% of challenge participants_
## OBJECTIVE : ##
>Fitzy Shortstack on Film Noir Island needs help battling dastardly phishers. Help sort the good from the bad!
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 14</summary>
  
>-	-	Discover the essentials of email security with DMARC, DKIM,a nd SPF at [Cloudflare’s Guide](https://www.cloudflare.com/en-gb/learning/email-security/dmarc-dkim-spf/).
</details>

#  

## PROCEDURE : ##
This one is quite straightforward to tackle.  Armed with basic background knowledge of how `DMARC`, `DKIM`, and `SPF` work we can go through the mails in the inbox one-by-one.  The easiest ones to mark as Phishing are those where the header includes: `DMARC: Fail`.  The rest need a slightly closer look.  In fact, we can also find a few emails where the domain in the **From** field does not match with that in the **Return-Path** value of the header.  These are also clearly phishing attempts.

Ultimately, we end up with **10 confirmed phishing emails.**
