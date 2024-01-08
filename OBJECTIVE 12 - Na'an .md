# OBJECTIVE 12 - Na'an #

## OBJECTIVE : ##
>Shifty McShuffles is hustling cards on Film Noir Island. Outwit that meddling elf and win!
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 12</summary>
  
>-  Try to outsmart Shifty by sending him an error he may not understand.
>-	Shifty said his deck of cards is made with Python. Surely there's a [weakness](https://www.tenable.com/blog/python-nan-injection) to give you the upper hand in his game.


</details>

#  

## PROCEDURE : ##

The name of this challenge almost gives the game away immediately especially when Shifty McShuffles mentions that he’s written the program in Python – we can immediately tell that this challenge will have something to do with exploiting a program by trying to pass a `NaN` (Not-a-Number) value.

When starting the game we are given five cards which accept a free-text input which is verified to determine that the input is a number between 0 and 9.  Once all five numbers are entered we can play our hand and we compare our results with Shifty’s.

As can be expected – notwithstanding his claims to the contrary - Shify is definitely cheating and we can verify this by playing the same hand multiple times and observing that Shifty plays the same hand too which means that **Shifty is able to see what cards we are going to play and modify his hand based on that**.

I wasn’t quite able to figure out the algorithm Shifty is using to play his hand but through some trial and error I noticed that he always plays the `0` and `9` and that if you play `0`,`1`,`8` and `9` he will copy those and try to play the smallest possible value as the fifth number – so that a hand with `0`,`1`,`2`,`8`,`9` will force Shifty to play the exact same hand and get a tie.

Armed with the above knowledge, I tried entering `nan` as the input of one of the cards and sure enough it was accepted.  Most probably the python code is checking whether `user_input < 0` and whether `user_input > 9` – both of which will return `False` when `user_input = nan`.
By playing a hand of `0`, `1`, `8`, `9` and `nan` we beat Shifty every time as he tries to play `0`,`1`,`2`,`8`,`9` and `nan` is evaluated as being **simulatenously the highest and lowest number** – earning us 2 points 😊

Just re-play the same hand 5 times to win the game.  **Shifty may be smart but he doesn’t learn** 😊

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/4a883a10-08b9-4d54-abb2-27e36bf8b256)

