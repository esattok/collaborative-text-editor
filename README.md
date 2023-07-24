# Collaborative Text Editor

- Collaborative Text editor enables multiple clients to edit a text file simultaneously
- Text Editor uses a custom application-level protocol which is built on top of TCP
- The processor performs several functions depending on the 16- bit instructions on 8-bit data
- The projet is implemented with System Verilog and tested on Vivado Basys3 FPGA board

# Program Lifecycle

1. First an authentication check will be done
2. A specific username (bilkentstu) and password (cs421f2022) will be looked after by the server
3. Authenticated clients can then edit the text by using several commands that are described below
   1. USER <username>
   2. PASS <password>
   3. WRTE <version><Space><linenumber><Space><text>
   4. APND <version><Space><text>
   5. UPDT <version>
   6. DSPLY <version>
   7. DSPLY <version><linenumber>
   8. CLR <version>
   9. CLR <version><linenumber>
   10. EXIT 
   
   
