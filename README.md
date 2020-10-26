# Computer-Network-Software
CSUN Comp 429 - projects/assignments

how to run

clone this repo

python ./ChatApplication.py <random port number, this is the port number you will be hosting your chat room>

run help in the shell to get a list of all commands

run help <command> to read the documentation of that command

the main commmands are

connect <remote_ip> <remote_port (the port of the connection room)>

then run list to see the connections connected to

then run send <number from list> <message> i.e. send 1 lol

using one machine

I did the following

cd .\Documents\comp_sci\Computer-Network-Software\

python .\ChatApplication.py 1111

python .\ChatApplication.py 2222

python .\ChatApplication.py 3333

connect 192.168.0.169 3333

use this line on all three terminals ^
