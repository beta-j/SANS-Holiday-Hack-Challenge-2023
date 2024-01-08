# OBJECTIVE 21 - Camera Access #

## OBJECTIVE : ##
>Gain access to Jack's camera. What's the third item on Jack's TODO list?
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 21</summary>
  
>-	-	In his hubris, Wombley revealed that he thinks you won't be able to access the satellite's "Supervisor Directory". There must be a good reason he mentioned that specifically, and a way to access it. He also said there's someone else masterminding the whole plot. There must be a way to discover who that is using the nanosat.
</details>

#  

## PROCEDURE : ##
This challenge starts at **Zenith SGS** on Space Island.  The vending machine provides us with a docker image and the middle console introduces us to **GateXOR the aligator** who gives us a **Wireguard** configuration which we can use to connect to the sever.  We can copy the client-side configuration to `/etc/wireguard/wg0.conf` and fire up wireguard VPN with `wg-quick up wg0`.

Now if we run the **NanoSat MO Base Station Tool** we can enter the following URI to bring up a list of providers: `maltcp://10.1.1.1:1024/nanosat-mo-supervisor-Directory`

Then click on **Connect to Selected Provider** and go to the **Apps Launcher Service** tab, select **Camera** and click the **runApp** button.  This will run the Camera App which we can now see if we go back to the **Communications Settings** tab.

Now we select **App:camera** and click on **Connect to Selected Provider** to bring up the possible actions we can invoke for the Camera App.

Under the **Action Service** tab we can see an action called `(Base64SnapImage)  (“Uses the NMF Camera service to take a jpg picture”)` so by selecting the action and clicking on the **submitAction** button we can get the camera to take a photo.

At this point it’s a good idea to start a Wireshark capture on interface `wg0` to start working on retrieving the contents of the photo image file.  Once Wireshark has started capturing packets, we can request the transfer of the raw image data from the server by going to the **Parameter Service** tab selecting `Base64SnapImage` and clicking on the **getValue** button.  A window pops up withe an extremely long string containg the `base64` encoded raw image data.  The window doesn’t allow us to copy the raw data off it – so this is were our Wireshark capture comes in handy.

At this point we can stop the Wireshark capture and right-click on one of the packets and select **Follow -> TCP Stream**.  It will take a few minutes for wireshark to bring up the full TCP stream as it’s a pretty large image file, but when it’s done we can choose to save it to a file – in my case I called this `output.txt`.

By using the following command I was able to extract the file to my local machine where I could remove any strings that where not part of the `base64` encoded image itself
```
$ docker cp 2bf63a2df16a:/root/output.txt /home/kali`
```

Finally it’s just a matter of using `base64 -d` to decode the string and output the result to a .jpg file:
```
$ base64 -d output.txt > image2.jpg
```
That’s it – by zooming in to the image we can see Jack’s To-Do list in all its **glooooooorrryy** 😊


![image2](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/3802ee8f-2a04-474d-931a-9ac5dbe3376a)
