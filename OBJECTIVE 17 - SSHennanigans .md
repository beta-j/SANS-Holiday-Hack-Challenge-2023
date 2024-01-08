# OBJECTIVE 17 - SSHennanigans #

## OBJECTIVE : ##
>Go to Pixel Island and review Alabaster Snowball’s new SSH certificate configuration and Azure Function App.  What type of cookie cache is Alabaster planning to implement?
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 16</summary>
  
>-	Azure CLI tools aren't always available, but if you're on an Azure VM you can always use the [Azure REST API](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) instead.
>-	The [get-source-control](https://learn.microsoft.com/en-us/rest/api/appservice/web-apps/get-source-control?view=rest-appservice-2022-03-01) Azure REST API endpoint provides details about where an Azure Web App or Function App is deployed from.
>-	Check out Thomas Bouve's [talk and demo](https://www.youtube.com/watch?v=4S0Rniyidt4) to learn all about how you can upgrade your SSH server configuration to leverage SSH certificates.
</details>

#  

## PROCEDURE : ##

Alabaster Snowball tells us that he needs our help with his “fancy new Azure server” at ``ssh-server-vm.santaworkshopgeeseislands.org``.  He also tells us that with the help of ChatNPT he has created a website that automatically generates certificates for users and that the website is found at: [https://northpole-ssh-certs-fa.azurewebsites.net/api/create-cert?code=candy-cane-twirl](https://northpole-ssh-certs-fa.azurewebsites.net/api/create-cert?code=candy-cane-twirl).  The [video by Thomas Bouve](https://www.youtube.com/watch?v=4S0Rniyidt4) is very helpful to get started with this one.

First order of business is to go ahead and create a certificate pair using `ssh-keygen` and the command shown in Thomas Bouve’s video:
```
$ Ssh-keygen -C ‘SSH Certificate CA’ -f ca
```

This will create two files; `ca` and `ca.pub`. Copy the contents of `ca.pub` into the form of the [certificate generator URL that Alabaster Snowball shared with us](https://northpole-ssh-certs-fa.azurewebsites.net/api/create-cert?code=candy-cane-twirl) and this will give us our SSH certificate.

We can go ahead and copy this text into a new file called `SSHCert.pub` and adjust permissions using `Chmod 600 SSHCert.pub`.  However, the text needs to be cleaned a bit before we can use this as our certificate file.  Remove the bit of text at the end that reads `“principal”: “elf”` and leave all the rest.  Save the file and we should be ready to connect to the server using our new certificate.

To connect use the following command to specify the private and public key pair to use with ssh:
```
$ ssh -i ca -i SSHCert.pub monitor@ssh-server-vm.santaworkshopgeeseislands.org 
```

This puts us through to Alabaster’s server and we are greeted by the **SatTrackr** dashboard. 

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/c2389d1c-729b-4d99-b44d-bb6958ec6c99)


Hitting the escape sequence `Ctrl+C` brings us to a terminal prompt, and we can start snooping around.  Right away we can see that there is another user called `alabaster` on this server which we do not have access permissions for.  
Also, by looking into `/etc/ssh/sshd_config.d/sshd_config_certs.conf` we can see that the server is set up to map principles to usernames by looking for the `AuthorizedPrincipalsFile` in `/etc/ssh/auth_principals/%u`.

The logical next step is to have a look at what’s inside the `auth_principals` folder and sure enough we can see two principals; `alabaster` and `monitor`.  By looking into the contents of these two principal files we can see that `alabaster` is mapped to the `admin` user and `monitor` is mapped to the `elf` user.
```
monitor@ssh-server-vm:/etc/ssh/auth_principals$ cat alabaster monitor 
admin
elf
```

Just to be sure we can check whether it is possible to edit the monitor principal to give us admin user access, but we do not have sufficient rights to edit the file and we’ll need to be a bit craftier.

So, let’s see what we can learn about the Azure server we’re on.  There is no Azure CLI available but as the hints kindly suggest we can use Azure REST API calls instead. By running the following command, we can retrieve the Azure Instance Metadata (IMDS)[^1] :
```
$ curl -s -H Metadata:true --noproxy "*" "http://169.254.169.254/metadata/instance?api-version=2021-02-01" | jq
```
*    Note: we pipe the output to jq to give us a nicely formatted JSON output.*

This gives us some useful information about the server we’re on.  Most importantly we learn our `subscriptionId` and `Resource Group Name`, which will be useful in the next few steps:
```
"resourceGroupName": "northpole-rg1",   
"resourceId": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/northpole-rg1/providers/Microsoft.Compute/virtualMachines/ssh-server-vm",   
    "subscriptionId": "2b0942f3-9bca-484b-a508-abdae2db5e64",
```

Next, we can go ahead and generate ourselves a token by calling a specific URI (I used `curl` and piped the output to `jq` for readability):
```
$curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2021-02-01&resource=https%3A%2F%2Fmanagement.azure.com%2F' -H Metadata:true -s | jq
```

This gives us an access_token that starts with `eyJ0...` (I will not be pasting the whole thing here as it’s a long string).  To make things a bit easier for ourselves we can assign the access token to a shell variable called `$TOKEN`:
```
$ TOKEN=eyJ0e.....
```

One of the hints for this challenge specifically mentions that we can use the REST API to get more information about the app that is running on the server and where it resides by using `Get Source Control` .  We can do this by calling a URI with the `subscriptionId` and `resourceId` parameters we learned earlier.  The `{name}` parameter is taken from the URL of the app, i.e. `northpole-ssh-certs-fa` and we also need to pass on the `$TOKEN` we generated earlier as a header in our request:
```
$ curl https://management.azure.com/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/northpole-rg1/providers/Microsoft.Web/sites/northpole-ssh-certs-fa/sourcecontrols/web?api-version=2022-03-01 -H "Authorization:Bearer $TOKEN” | jq 
```

From the output of this command we learn that the function app is being deployed from **`"repoUrl": "https://github.com/SantaWorkshopGeeseIslandsDevOps/northpole-ssh-certs-fa"`**. This allows us to have a closer look at the source code of the app by visiting its [GitHub repository](https://github.com/SantaWorkshopGeeseIslandsDevOps/northpole-ssh-certs-fa).  

The most interesting part of the code is that when the app receives an `HTTP POST` request it looks for the `principal` value in the input JSON – if it is not found it will set it to a default value `DEFAULT_PRINCIPAL`.  If only we could pass on a value for prinicpal ourselves!

I decided to use OWASP ZAP (Zed Attack Proxy) which I learned about in the [Reportinator Challenge]/ for this next step.  ZAP makes it easy to intercept and modify HTTP requests, so it was just a matter of loading the certificate-generating website in ZAP, submitting my public key in the corresponding field and then intercepting the HTTP POST request and just added “principal”:”admin” to the JSON in it before forwarding it.  The website immediately replies with our new certificate and we can see that the principal for the certificate is now ‘admin’.

Now we need to repeat the initial steps of this challenge with the new certificate to be able to log in as ‘alabaster’:
-	Copy the certificate to a file called SSHCert_admin.pub
-	Chmod 600 SSHCert_admin.pub
-	Log in to the server using the ‘alabaster’ username: 
ssh -i ca -i SSHCert_admin.pub alabaster@ssh-server-vm.santaworkshopgeeseislands.org
That’s it! We now have admin access to the server, and we can see alabaster’s to-do list in his home folder, from which we find out that he intends to implement a “Gingerbread Cookie Cache”.
~$ cat alabaster_todo.md 
# Geese Islands IT & Security Todo List

- [X] Sleigh GPS Upgrade: Integrate the new "Island Hopper" module into Santa's sleigh GPS. Ensure Rudolph's red nose doesn't interfere with the signal.
- [X] Reindeer Wi-Fi Antlers: Test out the new Wi-Fi boosting antler extensions on Dasher and Dancer. Perfect for those beach-side internet browsing sessions.
- [ ] Palm Tree Server Cooling: Make use of the island's natural shade. Relocate servers under palm trees for optimal cooling. Remember to watch out for falling coconuts!
- [ ] Eggnog Firewall: Upgrade the North Pole's firewall to the new EggnogOS version. Ensure it blocks any Grinch-related cyber threats effectively.
- [ ] Gingerbread Cookie Cache: Implement a gingerbread cookie caching mechanism to speed up data retrieval times. Don't let Santa eat the cache!
- [ ] Toy Workshop VPN: Establish a secure VPN tunnel back to the main toy workshop so the elves can securely access to the toy blueprints.
- [ ] Festive 2FA: Roll out the new two-factor authentication system where the second factor is singing a Christmas carol. Jingle Bells is said to be the most secure.
 

[^1]: [https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux ](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux )
