# Computer-Network-Software - CSUN Comp 429

COMP429 Programming Assignment 1
A Chat Application for Remote Message Exchange

Carlos Benavides
Matthew

# Contributions

Carlos - Created the barebones of the project, created the client/server and the terminal/unix shell for this project. Was able to create the functionality of joining, and leaving a certain chat room process, and send a message to connected processes.


### How to run

clone this repo

cd .\Computer-Network-Software\

must have python (python3 preferred)

`python ./chat.py <desired port number, this is the port number you will be hosting your chat room>`

for example

`python ./chat.py 5656`

1) run `help` in the shell to get a list of all commands

run `help <command>` to read the documentation of that command

2) run `myip` to see the ip of your machine

3) run `myport` to see the port you have chosen for your chatroom

4) run `connect <remote_ip> <remote_port>` to connect to a different user's chatroom

5) run `list` to see the all the connections the process if part of

6) run `terminate <connection_id>` to terminate connection to a certain host (connection_id is from the list command)

7) run `send <message> <connection_id>` to send a message to a certain host (connection_id is from the list commands)

Demo in terminal:

![Imgur Image](https://i.imgur.com/bE2bHk0.png)


Sources:

StackOverflow
1) to find how to retrieve ip from python - https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

GeeksForGeeks
1) to understand how to make a thread class and stop a thread in python - https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/

Medium - Let’s Write a Chat App in Python
1) to understand how sockets work in python - https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
