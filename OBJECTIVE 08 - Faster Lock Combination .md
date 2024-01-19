# OBJECTIVE 8 - Faster Lock Combination #
_Completed by 7.58% of challenge participants_
## OBJECTIVE : ##
>Over on Steampunk Island, Bow Ninecandle is having trouble opening a padlock. Do some research and see if you can help open it! 
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 8</summary>
  
>-  -	I'm sure there are some clever tricks and tips floating around [the web](https://www.youtube.com/watch?v=27rE5ZvWLU0) that can help us crack this code without too much of a flush... I mean fuss.

</details>

#  

## PROCEDURE : ##

Here’s another cool lock-picking simulation!
This time Bow Ninecandle gives us a handy link showing a video demonstration of how to decode and unlock a combination lock.  The video also includes a link to another video that shows the correct way of opening such a lock once you have the combination – this proved to be an important resource in my case.

The first step is to apply moderate pressure to the shackle and rotate the dial until it gets stuck on a number.  In our case this was **31** which we will call our *“Sticky Number”*. Next we turn the dial back to zero and apply as much pressure as possible on the shackle and rotate the dial counter-clockwise until we find two numbers between 0 and 11 where the dial appears to stick half-a number below and half a number above.  In our case these two numbers were **Guess No. 1 = 5** and **Guess No. 2 = 6**.

To obtain the first digit of our combination we simply add 5 to our “Sticky Number”:


```
31 + 5  = 36
```

Therefore **1st digit = 36**

 
To obtain our third digit we need to divide the 1st digit we obtained just now by 4 and determine the remainder:

```
36 / 4 = 9 remainder 0
```

Now we need to list two rows of numbers.  The first row will have our **Guess No. 1** and then the same number added to 10, 20 and 30.  
Similarly the second row will have our **Guess No. 2** and then the same number added to 10,20, and 30.  

Since our guess numbers were 5 and 6, we get the following:

5 |	15|	25|	35
---|---|---|---|
6|	16|	26|	36

For each of the above numbers we need to try dividing by 4 and selecting those numbers that give us a remainder equal to that obtained in the previous step (in our case, this is 0).  The only two numbers listed above that leave a remainder of 0 when divided by 4, are **16** and **36**.

It is unlikely that 36 is used twice in our combination, but we can test this by going to 16 on the lock, applying pressure to the shackle and wiggling the dial to either side.  We then repeat the same operation with 36 and we can notice a clear difference between the two scenarios with the dial appearing considerably easier to move when on the 16.  This indicates that **16 is our 3rd digit**.

This leaves us to determine the possible values for our 2nd digit.  We can do this by listing two rows of numbers as follows:

-	First Row:  Take the remainder obtained earlier and add it to 2 (in our case; `0+2 = 2`).  Then write this number down, followed by the same number added to 8, 16, 24 and 32 respectively.
  
-	Second Row: Take the remainder obtained earlier and add it to 6 (in our case; `0+6 = 6`).  Then write this number down, followed by the same number added to 8, 16, 24 and 32 respectively.

ROW 1:|		2|	10|	18|	26|	34
---:|:---:|:---:|:---:|:---:|:---:|
ROW 2:|		6|	14|	22|	30|	38

Our second digit can be any of the numbers in these two rows with the exception of any numbers that are two numbers or less away from the third digit of the combination.  Since our third digit is 16, we can eliminate 14 and 18 from the above list, which leaves us with the following:

ROW 1:|		2|	10|	~~18~~|	26|	34|
---:|:---:|:---:|:---:|:---:|:---:|
ROW 2:|		6|	~~14~~|	22|	30|	38|

Digit | Possible Values
:---:|:---
1st Digit:|	36
2nd Digit:|	2, 6, 10, 22, 26, 30, 34, or 38
3rd Digit:|	16

So now we just need to try 8 different combinations on the lock.

In my case I was lucky enough to open the lock on the third attempt.  So, the final lock combination is:  **36-10-16**

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/3bdf2c6d-4a96-4eca-899f-7b4fb369bc83)

