# OBJECTIVE 9 - Game Cartridge Vol 1 #
_Completed by 5.73% of challenge participants_
## OBJECTIVE : ##
>Find the first Gamegosling cartridge and beat the game.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 9</summary>
  
>-  Listen for the gameboy cartridge detector's proximity sound that activates when near buried treasure. It may be worth checking around the strange toys in the Tarnished Trove.
>-  Giving things a little push never hurts.
>-  Out of sight but not out of ear-shot
>-  You think you fixed the QR code? Did you scan it and see where it leads?
</details>

#  

## PROCEDURE : ##

As per the hints – the game cartridge is found hiding in one of the weird toys scattered around Tarnished Trove.

Looking at the iframe code for `script.js` we can see a global constant defined as const `ROM_FILENAME = "rom/game.gb"`; 
This tells us that we can download the [ROM file](Assets/Vol1%20-%20game.gb) from [https://gamegosling.com/vol1-uWn1t6xv4VKPZ6FN/rom/game.gb](https://gamegosling.com/vol1-uWn1t6xv4VKPZ6FN/rom/game.gb) and load it up in any Gameboy emulator to be able to save and load states within the game making it *a lot* easier to complete.

After playing the game and carefully moving all the 7 blocks to their correct positions we get to see the completed QR code – which when scanned gives us a link to [https://8bitelf.com/](https://8bitelf.com/) which is a page that just contains our flag which we need to pass on to our objective to complete it:

```
flag:santaconfusedgivingplanetsqrcode
```
