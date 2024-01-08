# OBJECTIVE 13 - KQL Kraken Hunt #

## OBJECTIVE : ##
>Use Azure Data Explorer to [uncover misdeeds](https://detective.kusto.io/sans2023) in Santa's IT enterprise. Go to Film Noir Island and talk to Tangle Coalbox for more information 
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 13</summary>
  
>-	Do you need to find something that happened via a process? Pay attention to the *ProcessEvents* table!
>-	Once you get into the [Kusto trainer](https://detective.kusto.io/sans2023), click the blue *Train me for the case* button to get familiar with KQL.
>-	Looking for a file that was created on a victim system? Don't forget the *FileCreationEvents* table.
</details>

#  

## PROCEDURE : ##

The name of this challenge almost gives the game away immediately especially when Shifty McShuffles mentions that he’s written the program in Python – we can immediately tell that this challenge will have something to do with exploiting a program by trying to pass a `NaN` (Not-a-Number) value.

