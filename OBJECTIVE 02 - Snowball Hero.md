# OBJECTIVE 2 - Snowball Hero #

## OBJECTIVE : ##
>Visit Christmas Island and talk to Morcel Nougat about this great new game. Team up with another player and show Morcel how to win against Santa!
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 2</summary>
  
>-	Its easiest to grab a friend play with and beat Santa but tinkering with client-side variables can grant you all kinds of snowball fight super powers. You could even take on Santa and the elves solo!

>-	Have an iframe in your document? Be sure to select the right context before meddling with JavaScript.
</details>

#  

## PROCEDURE : ##

By inspecting the code in the browser’s console I was able to identify a number of client-side variables that could be manually updated to make it a lot easier to win the game.   Some of the variable changes I made in the browser console where:

`elfThrowDelay = 999999`

`santaThrowDelay = 999999`

`playersHitBoxSize = [0,0,0,0]`

This effectively rendered me invincible and disabled the elves and Santa from throwing any snowballs.  This way I was able to simply wait for someone to join the fight and we could defeat Santa together.

The hints seem to indicate that there should also be a way of defeating Santa on my own  but I didn’t manage to achieve that.  I identified a client-side variable called `singlePlayer` and if I manually set this to `‘true’` before clicking on the Ready button, the game would play a sound saying **“Never Fear! Elf the Dwarf is here!”**  and based on the code snippet below I’m guessing the game should theoretically generate a sprite (`jaredSprite`) to assist me in fighting Santa.  But no matter how many times I tried, the game just froze up completely and became unplayable whenever I changed this variable ☹
      
      ReadyButton.on('pointerdown', function() {
        ReadyButton.destroy();
        scrollintro.destroy()
        player.update = true
        player.ready = 1
        // jared ... I mean Elf the dwarf joins the fight when in single player mode
        if (singlePlayer === 'true') {
          setTimeout(() => {
            if (isaudio) {
              gameSceneObject.sound.play('elf_the_dwarf_is_here', { volume: 0.5 });
            }
            toastManager.showToast("Elf the dwarf has joined your team!", duration=500, delay=5000);
            jaredSprite = gameSceneObject.physics.add.sprite(starting_pos.x + 150, starting_pos.y, 'jaredSprite');
            //jaredSprite.setScale(1.2)
            jaredSprite.setScale(0)
            jaredSprite.setAlpha(0)
            gameSceneObject.tweens.add({
 

