# BONUS! Fishing Mastery #
_Completed by 1.42% of challenge participants_
## OBJECTIVE : ##
>Catch at least one of each species of fish that live around Geese islands. When you're done, report your findings to Poinsettia McMittens.

#  

## PROCEDURE : ##
By looking at the html code of the game we see a comment referring to `fishdensityref.html for Developers Only!` – interesting.  
This page can be accessed by going to [https://2023.holidayhackchallenge.com/sea/fishdensityref.html](https://2023.holidayhackchallenge.com/sea/fishdensityref.html) and gives us a list of all the available fish along with heat maps of where to find them.  These heat maps can be overlayed onto the minimap to help pin-point the ideal fishing locations of the fish including the very elusive **_Piscis Cyberneticus Skodo_**.

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/1f1096ba-1c89-4b76-b65c-7908a3ba1cb5)


From the `fishdensityref.html` page we can determine that there are 171 types of fish that can be caught – it will take us way too long to actually fish for them one by one, so we have to look at possible ways of automating this. 

By looking at the source code in the browser console, I noticed three particular elements that where of interest: `castReelBtn.click()` action that activated the **Cast Reel** button, `reelItInBtn.click()` action that activated the **Reel It In** button and the `reelItInBtn.classList.contains(‘gotone’)` property that turns `true` when a fish is on the line (and causes the **Reel it In** Button to turn red).  Since I’m hopeless at JavaScript I just fed these three elements to ChatGPT and asked it to write a script that would perform the action `castReelBtn.click()` then wait for `reelItInBtn.classList.contains(‘gotone’)` to become true before calling `reelItInBtn.click()` and repeating in a loop.  

ChatGPT kindly came up with the requested JavaScript function which I could then simply paste into the browser’s console and then call it with `simulateFishing(iterations)`, where `iterations` is the number of times I want it to repeat the loop.  I spent some time fishing at the spot just off the shore of Steampunk Island until I caught a *Piscis Cyberneticus Skodo*.

Next, I downloaded all the fish density maps from `fishdensityref.html` and asked ChatGPT to write a script that will superimpose all the images to determine the areas where there is the largest fish variety. I also asked it to create a variation of the script that highlighted the top 500 ‘hottest’ pixels on the resulting stacked image which gave a very interesting result showing that the best fishing spot in all of Geese Islands is just off the shore of the **Blacklight District of Film Noir Island**.  I spent some time fishing there using the automated fishing script and when I just had the last three fish to go, I used the fish density maps to move my ship to areas where those remaining fish are most abundant until I had caught all 171 fish.

![White patch includes the best fishing spot in all of Geese Islands](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/ee3a0f74-931d-476d-9490-d3205a0891ef)


Btw – whilst scrolling through the code I found this pun hidden in a variable name: **`pescadexFINdexSeeWhatIDidThere`**

Yep – I laughed XD

