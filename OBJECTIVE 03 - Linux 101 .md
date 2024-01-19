# OBJECTIVE 3 - Linux 101 #
_Completed by 44.45% of challenge participants_

## OBJECTIVE : ##
>Visit Ginger Breddie in Santa's Shack on Christmas Island to help him with some basic Linux tasks. It's in the southwest corner of Frosty's Beach.
#  

## PROCEDURE : ##

>Type "yes" to begin:

`yes`

>Perform a directory listing of your home directory to find a troll and retrieve a present!

`~$ ls`

```HELP  troll_19315479765589239  workshop```

>Now find the troll inside the troll.

`~$ cat troll_19315479765589239`

```troll_24187022596776786```

>Great, now remove the troll in your home directory.

`~$ rm troll_19315479765589239`

>Print the present working directory using a command.

`~$ pwd`

```/home/elf```

>Good job but it looks like another troll hid itself in your home directory. Find the hidden troll!

`~$ ls -a`

```.  ..  .bash_history  .bash_logout  .bashrc  .profile  .troll_5074624024543078  HELP  workshop```

>Excellent, now find the troll in your command history.

`~$ history`

```
    1  echo troll_9394554126440791
    2  ls
    3  cat troll_19315479765589239 
    4  rm troll_19315479765589239 
    5  pwd
    6  ls -a
    7  history
```

>Find the troll in your environment variables.

`~$ printenv | grep "troll"`

```z_TROLL=troll_20249649541603754```

>Next, head into the workshop.

`~$ cd workshop/`

>A troll is hiding in one of the workshop toolboxes. Use "grep" while ignoring case to find which toolbox the troll is in.

`~/workshop$ cat toolbox_* | grep 'troll' --ignore-case`

```tRoLl.4056180441832623```

>A troll is blocking the present_engine from starting. Run the present_engine binary to retrieve this troll.

```~/workshop$ ls -a | grep 'present*'
present_engine
~/workshop$ ./present_engine
bash: ./present_engine: Permission denied
~/workshop$ chmod +x present_engine
~/workshop$ ./present_engine
troll.898906189498077
```

>Trolls have blown the fuses in /home/elf/workshop/electrical. cd into electrical and rename blown_fuse0 to fuse0.

```
~/workshop$ cd /home/elf/workshop/electrical/
~/workshop/electrical$ mv blown_fuse0 fuse0
```

>Now, make a symbolic link (symlink) named fuse1 that points to fuse0

`~/workshop/electrical$ ln -s fuse0 fuse1`

>Make a copy of fuse1 named fuse2.

`~/workshop/electrical$ cp fuse1 fuse2`

>We need to make sure trolls don't come back. Add the characters "TROLL_REPELLENT" into the file fuse2.

`~/workshop/electrical$ echo "TROLL_REPELLENT" >> fuse2`

>Find the troll somewhere in /opt/troll_den.

```
/opt/troll_den$ find /opt/troll_den/ -iname "*troll*"
/opt/troll_den/
/opt/troll_den/plugins/embeddedjsp/src/main/java/org/apache/struts2/jasper/compiler/ParserController.java
/opt/troll_den/apps/showcase/src/main/resources/tRoLl.6253159819943018
/opt/troll_den/apps/rest-showcase/src/main/java/org/demo/rest/example/IndexController.java
/opt/troll_den/apps/rest-showcase/src/main/java/org/demo/rest/example/OrdersController.java
Find the file created by trolls that is greater than 108 kilobytes and less than 110 kilobytes located somewhere in /opt/troll_den.
/opt/troll_den$ find /opt/troll_den/ -size +108k -size -110k
/opt/troll_den/plugins/portlet-mocks/src/test/java/org/apache/t_r_o_l_l_2579728047101724
```

>List running processes to find another troll.

```
/opt/troll_den$ ps -e
    PID TTY          TIME CMD
      1 pts/0    00:00:00 tmuxp
  17469 pts/2    00:00:00 14516_troll
  17991 pts/3    00:00:00 ps
```

>The 14516_troll process is listening on a TCP port. Use a command to have the only listening port display to the screen.

```
/opt/troll_den$ netstat -tl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:54321           0.0.0.0:*               LISTEN     
```

>The service listening on port 54321 is an HTTP server. Interact with this server to retrieve the last troll.

`/opt/troll_den$ curl 0.0.0.0:54321`

>Your final task is to stop the 14516_troll process to collect the remaining presents.

```
/opt/troll_den$ kill 17469
Type "exit" to close...
/opt/troll_den$ exit
``` 
