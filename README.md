# Collaborative Text Editor

## Overview

- Collaborative Text editor enables multiple clients to edit a text file simultaneously
- Text Editor uses a custom application-level protocol which is built on top of TCP
- Python is used as the programming language
- Socket module is used for socket programming

## Program Lifecycle

1. First an authentication check will be done
2. A specific username (bilkentstu) and password (cs421f2022) will be looked after by the server
3. Authenticated clients can then edit the text by using several commands which will be described
4. When the editing is done, user can exit the program

## Allowed Commands

1. USER \<username\>
2. PASS \<password\>
3. WRTE \<version\> \<Space\> \<linenumber\> \<Space\> \<text\>
4. APND \<version\> \<Space\> \<text\>
5. UPDT \<version\>
6. DSPLY \<version\>
7. DSPLY \<version\> \<linenumber\>
8. CLR \<version\>
9. CLR \<version\> \<linenumber\>
10. EXIT 

## Running the Application

### Running the Server Program

`python Server.py <Addr> <ControlPort>`
- \<Addr\>: The IP address of the server.
- \<ControlPort\> The control port to which the server will bind.

### Running the Client Program

`python3 TextEditor.py <Addr> <ControlPort>`
- \<Addr\>: The IP address of the server.
- \<ControlPort\> The control port to which the server will bind.

   
