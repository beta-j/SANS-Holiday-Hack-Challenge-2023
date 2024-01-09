# OBJECTIVE 20 - Space Island Door Speaker #

## OBJECTIVE : ##
>There's a door that needs opening on Space Island! Talk to Jewel Loggins there for more information.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 20</summary>
  
>-	It seems the Access Speaker is programmed to only accept Wombley's voice. Maybe you could get a sample of his voice and use an AI tool to simulate Wombley speaking the passphrase.
</details>

#  

## PROCEDURE : ##
For this challenge we need to open a door by speaking a passphrase with Wombley’s voice.  Jewel Loggins helpfully suggests that we can use some kind of AI tool to achieve this.

We already know the passphrase from [OBJECTIVE 19 – Active Directory](OBJECTIVE%2019%20-%20Active%20Directory%20.md) and we have a [sample of Wombley’s voice](Assets/wombleycube_the_enchanted_voyage.mp3) that was given to us by Piney Sappington when completing [OBJECTIVE 16 – Elf Hunt](OBJECTIVE%2016%20-%20Elf%20Hunt%20.md).

I tried using two different AI voice synthesizers for this one:

•	**PlayHT**: [https://play.ht/](https://play.ht/) and 

•	**AlphaDragon Voice-Clone**: [https://huggingface.co/spaces/AlphaDragon/Voice-Clone](https://huggingface.co/spaces/AlphaDragon/Voice-Clone)

With both synthesizers it’s a simple case of uploading [Wombley’s voice sample](Assets/wombleycube_the_enchanted_voyage.mp3), and entering the following passphrase:
```
And he whispered, 'Now I shall be out of sight;
So through the valley and over the height.'
And he'll silently take his way.
```

This will generate a [.wav file which we can use to unlock the door](Assets/AI-generated-passphrase.wav).

 ![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/637d800a-f1c8-41e8-b7b5-b2d873ad7bed)

