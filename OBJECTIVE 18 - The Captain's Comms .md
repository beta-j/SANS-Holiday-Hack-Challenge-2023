# OBJECTIVE 18 - The Captain's Comms #
_Completed by 2.61% of challenge participants_
## OBJECTIVE : ##
>Speak with Chimney Scissorsticks on Steampunk Island about the interesting things the captain is hearing on his new Software Defined Radio. You'll need to assume the **GeeseIslandsSuperChiefCommunicationsOfficer** role.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 18</summary>
  
>-	I hear the Captain likes to abbreviate words in his filenames; shortening some words to just 1,2,3, or 4 letters.
>-	Web Interception proxies like Burp and Zap make web sites fun!
>-	I've seen the Captain with his Journal visiting Pixel Island!
>-	A great introduction to JSON Web Tokens is available from Auth0.
>-	Find a private key, update an existing JWT!
</details>

#  

## PROCEDURE : ##

By intercepting in **BURP** we can see the value of a Bearer token in an authorization header:  `Authorizaion: Bearer eyJhbG.....`

From the [Just Watch This: Owner’s Card](Assets/ownCard.png) we also learn that the `radioMonitor` role token is stored in `/jwtDefault/rMonitor.tok` which we can retrieve using `curl` and the bearer token we just got:

```
curl https://captainscomms.com/jwtDefault/rMonitor.tok -H "Authorization: Bearer eyJhb..."
```

By pasting the output to [jwt.io](https://jwt.io) (or performing a `base64` decode) we can see that the JWT we obtained contains the following:
```
{
  "alg": "RS256",
  "typ": "JWT"
}
{
  "iss": "HHC 2023 Captain's Comms",
  "iat": 1699485795.3403327,
  "exp": 1809937395.3403327,
  "aud": "Holiday Hack 2023",
  "role": "radioMonitor"
}
```

This confirms that we now have the JWT token required for the `radioMonitor` role.  The logical next step is to edit the contents of the `justWatchThisCookie` and replace it with the JWT for `radioMonitor`. With this new cookie set we can access the waterfall and behold a pretty greeting from SANS – but nothing more without the `radioDecoder` token.

By this point we’re starting to figure out that the Captain is somewhat careless wit how he stores his tokens and keys – so it’s worth just trying to see whether we can get the `radioDecoder.tok` token with the same URI call we used for `radioMonitor.tok`.

```
$ curl https://captainscomms.com/jwtDefault/rDecoder.tok -H "Authorization: Bearer eyJhb..”
```

Sure enough, we now have the JWT token for the `radioDecoder role`.  We can simply repeat the previous steps and update the `justWatchThisCookie` value with the newly acquired JWT.  This now allows us to access the waterfall again and decode the signals that is receiving.  There are three signals being received:

### Morse transmission: ###
```
... CQ CQ CQ DE KH644 – SILLY CAPTAIN! WE FOUND HIS FANCY RADIO PRIVATE KEY IN A FOLDER CALLED TH3CAPSPR1V4T3F0LD3R...   
```
### RadioFax Transmission: ###
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/60ab084e-36b0-4b4e-8d54-11e76aebbaf1)

### Voice Transmission:  ###
```
{music} {music} {music} 88323 88323 88323 {gong} {gong} {gong} {gong} {gong} {gong} 12249 12249 16009 16009 12249 12249 16009 16009 {gong} {gong} {gong} {gong} {gong} {gong} {music} {music} {music}          
```
#  
Next, we need to figure out a way to get the Administrator Role to operate the radio transmitter.  In the Captain’s **ChatNPT Initial To-Do List** we read that the captain 
>“moved the private key to a folder [he] hope[s] no one will find.  [He] created a ‘keys’ folder in the same directory the roleMonitor token is in and put the public key ‘capsPubKey.key‘ there”

So, we can just `curl` to `/jwtDefault/keys/capsPubKey.key` to get the Public Key – easy!
```
$ curl https://captainscomms.com/jwtDefault/keys/capsPubKey.key -H "Authorization: Bearer eyJhbGc..."
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0.....
-----END PUBLIC KEY-----
```

By this point we have a pretty good idea of how the captain stores and names his files so we can hazard a guess that if he named the public key file `capsPubKey.key`, the Private key is probably called `capsPrivKey.key`.  We also learned from the morse transmission that it’s in a folder called `TH3CAPSPR1V4T3F0LD3R`.

We can now quite easily guess at the full URI for the Private Key file:
```
$ curl https://captainscomms.com/jwtDefault/keys/TH3CAPSPR1V4T3F0LD3R/capsPrivKey.key -H "Authorization: Bearer eyJhbGc..."
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgk...
-----END PRIVATE KEY-----
```

Armed with the Public/Private key pair we can use [jwt.io](https://jwt.io) to create a new JWT for the administrator role.  We just need to guess at what that role might be called.  There are plenty of hints for this in the [Captain’s Log](Assets/captains-Log.png) which lead us to understnd that the administrator’s role is called `GeeseIslandsSuperChiefCommunicationsOfficer`.

Using jwt.io create, encode and sign the following token:
```
{
  "alg": "RS256",
  "typ": "JWT"
}   
{
  "iss": "HHC 2023 Captain's Comms",
  "iat": 1699485795.3403327,
  "exp": 1809937395.3403327,
  "aud": "Holiday Hack 2023",
  "role": "GeeseIslandsSuperChiefCommunicationsOfficer"
}
```

Once again, we replace the contents of `justWatchThisCookie` with the newly crafted JWT and we are able to use the transmitter.
From the RadioFax transmission we know that the Frequency is `10426Hz`.  The Go-Time and Date are probably what is being transmitted by the numbers station, i.e. `12/24` and `16:00`.  Since we are instructed (in the [Background Instructions](Assets/Background_Instructions.png)) to transmit a time that is four hours earlier, we transmit the following values: 

**`Freq: 10426Hz / Date: 1224 / Time: 1200`**

And that successfully completes this challenge.

                                                                                                                            
![superCaptainStopsTheBadGuysHHC202399](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/67a0a803-66a3-4f4f-99eb-1c226cb62fae)

