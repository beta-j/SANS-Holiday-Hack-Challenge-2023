# OBJECTIVE 15 - Hashcat #
_Completed by 18.42% of challenge participants_
## OBJECTIVE : ##
>Eve Snowshoes is trying to recover a password.  Head to the Island of Misfit Toys and take a crack at it!
#  

## PROCEDURE : ##
This is a pretty easy one – we are conveniently given a hash file (`hash.txt`) to crack and a password list  (`password_list.txt`) to go with it and we are instructed to use **Hashcat** to crack the password.

First thing to do is to determine the hash type.  This is easily achieved by looking at the contents of the `hash.txt` file and observing the string at the start of the file:

```console
~$ cat hash.txt 
$krb5asrep$23$alabaster_snowball@XMAS.LOCAL:22865a2bceeaa73227ea4021879eda02$8f07417379e610e2dcb0621462fec3675bb5a850aba31837d541e50c622dc5faee60e48e019256e466d29b4d8c43cbf5bf7264b12c21737499cfcb73d95a903005a6ab6d9689ddd2772b908fc0d0aef43bb34db66af1dddb55b64937d3c7d7e93a91a7f303fef96e17d7f5479bae25c0183e74822ac652e92a56d0251bb5d975c2f2b63f4458526824f2c3dc1f1fcbacb2f6e52022ba6e6b401660b43b5070409cac0cc6223a2bf1b4b415574d7132f2607e12075f7cd2f8674c33e40d8ed55628f1c3eb08dbb8845b0f3bae708784c805b9a3f4b78ddf6830ad0e9eafb07980d7f2e270d8dd1966elf@8044fc109d9a:~$
```

The file starts with **`$krb5asrep$23`** which means that it is a **Kerberos ASREP** token (as hinted at in the opening introduction of the challenge) which corresponds to `Hash-Mode 18200` in HashCat.

The opening introduction also advises us to use the `-w 1 -u 1 --kernel-accel 1 --kernel-loops 1` switches with HashCat to keep system usage low.

So, all that we need to do to crack the password is run the following command:

```console
~$ hashcat -a 0 -w 1 -u 1 --kernel-accel 1 --kernel-loops 1 -m 18200 hash.txt password_list.txt --force
```

Once HashCat runs and confirms that we have a match, we can see the password stored in `~/.hashcat/hashcat.potfile`.

And that’s it – we’ve learnt that Alabaster Snowball’s password is **`IluvC4ndyC4nes!`**, which we can confirm by running `/bin/runtoanswer` and submitting the password.

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023/assets/60655500/f7bed17f-fdd0-4a51-a036-c88df337a44b)

 

 


