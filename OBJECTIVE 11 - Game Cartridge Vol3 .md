# OBJECTIVE 11 - Game Cartridge Vol 3 #

## OBJECTIVE : ##
>Find the third Gamegosling cartridge and beat the game.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 11</summary>
  
>-  The location of the treasure in Rusty Quay is marked by a shiny spot on the ground. To help with navigating the maze, try zooming out and changing the camera angle.
>-  This one is a bit long, it never hurts to save your progress!
>-  8bit systems have much smaller registers than you’re used to.
>-  Isn’t this great?!? The coins are **OVERFLOW**ing in their abundance.

</details>

#  

## PROCEDURE : ##

Just like what we did in [Game Cartridge Vol 1](OBJECTIVE%2009%20-%20Game%20Cartridge%20Vol%201%20.md), we can look at the source code to see a global constant defined as const `ROM_FILENAME = "rom/game.gb"`;  This tells us that the game’s ROM file can be downloaded from the `/rom/game.gb` directory at the following URL: [https://gamegosling.com/vol3-7bNwQKGBFNGQT1/rom/game.gb](https://gamegosling.com/vol3-7bNwQKGBFNGQT1/rom/game.gb)

Once we have the [ROM file](Assets/Vol3%20-%20game.gb) we can load into a GameBoy Emulator ([I used BGB for this](https://bgb.bircd.org/)) which lets us look at the values stored in the game’s memory and also allows us to save and load the game’s state making it a lot easier to get through the game.  

The [BGB website has an extremely useful guide](https://bgb.bircd.org/manual.html#cheats) for this bit.

BGB allows us to search for memory registers holding a specific value, then filter by those registers that have remained unchanged or by those registers that have increased or decreased in value.

My first instinct was to try and get to the end of the game whilst trying to figure out what memory registers are storing the value of the coins (we always could use more coins, right?).  The game ends at a particular point where elf needs to jump off a cliff into nothingness...surely there must be a way around this!

By following the [BGB cheat guide](https://bgb.bircd.org/manual.html#cheats) and after some trial and error I figured out that the coins’ value is being stored as follows:

Digit | Registers
---|---
Leftmost digit (representing hundreds) |	C160 and CB9E
Middle digit (representing tens) |		C12C and CB9C
Rightmost digit (representing units)|	C1F8 and CBA2

Now we can change and freeze the values of these 6 registers to `09` (to give ourselves **999 coins**) and play through the game saving states regularly to avoid being killed and having to start over.  

When we reach the end of the game we now see some floating platforms in the chasm – I’m assuming these were conveniently created by a buffer overflow caused when fixing the registers to `09`.  We are now able to jump across the chasm using the floating platforms, talk to a hacker to get a passcode, give the passcode to ChatNPT who in turn allows us to move a large rock to get this objectives flag!  

**MUCH GLOOOOOOOOORYYY** 😊

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/3987a800-99f6-42cd-8c45-88688a6fa2e8)


