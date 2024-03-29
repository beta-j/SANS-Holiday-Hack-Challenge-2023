# OBJECTIVE 10 - Game Cartridge Vol 2 #
_Completed by 2.72% of challenge participants_
## OBJECTIVE : ##
>Find the second Gamegosling cartridge and beat the game.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 10</summary>
  
>-  Try poking around Pixel Island. There really aren't many places you can go here, so try stepping everywhere and see what you get!
>-	This feels the same, but different! 2) If it feels like you are going crazy, you probably are! Or maybe, just maybe, you've not yet figured out where the hidden ROM is hiding. 3) I think I may need to get a DIFFerent perspective. 4) I wonder if someone can give me a few pointers to swap.

</details>

#  

## PROCEDURE : ##
If we look at the `script.js` file in the browser’s console we can see a global variable being declared at the start: `Const ROM_FILENAME = “rom/game”;`

Further down on line 142 we find the following:

```javascript
  let ranNum = Math.round(Math.random()).toString()
  let filename = ROM_FILENAME + ranNum + ".gb";
  console.log(filename);
```
The author must have intended to append a set of random digits to the filename to make it hard to guess, but the random number generator is implemented incorrectly.  `Math.random()` will generate a random number between 0 and 1 and `Math.round()` will round it to the nearest integer so the filenames generated by this function can only ever be `game0.gb` or `game1.gb`.

The script also outputs the result to console (probably a left-over artefact from when the author was troubleshooting the script) – but it’s useful for us to verify the above.

We can now download the rom files for the game from the following URLS:

[https://gamegosling.com/vol2-akHB27gg6pN0/rom/game0.gb](https://gamegosling.com/vol2-akHB27gg6pN0/rom/game0.gb)

[https://gamegosling.com/vol2-akHB27gg6pN0/rom/game1.gb](https://gamegosling.com/vol2-akHB27gg6pN0/rom/game1.gb)

Copies may also be found here:  [game0](Assets/Vol2%20-%20game0.gb)  and [game1](Assets/Vol2%20-%20game1.gb)

If necessary, the webpage with the game can be reloaded several times until the console shows `rom/game0.gb` or `rom/game1.gb` depending on which version of the game we want to test.

**Game0** has some immediately apparent differences to **Game1**, with the wizard and the elf being positioned on the opposite sides of the passage.

After downloading the two rom files we can covert them using xxd and compare the outputs:

```console
$ xxd game0.gb > game0.hex
$ xxd game1.gb > game1.hex
$ diff game0.hex game1.hex
```

If we modify the following entry and run the game:

```console
Hex0: < 00016a80: 2080 0c80 0300 000f f807 0000 0000 0f10   ...............
---
Hex1: > 00016a80: 2080 0c80 0b00 000f f807 0000 0000 0f10   ...............
```

We get a portal which takes us to a pokeball that called “ChatNPT” that just loves “old-timey” radio.  If we interact with the radio, it starts transmitting a series of beeps.  

Luckily, I got my morse code certification from the [local radio club](http://9h1mrl.org/) a couple of years ago and I was immediately able to recognise this as a Morse Code transmission of “`GL0RY`” – nice one! 

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/fae9f21a-ce37-47e9-bb92-da4bc3f3c94a)

 
