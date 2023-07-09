from socket import *
import sys

ENCODING = "ascii"
NEWLINE = "\r\n"

# Socket address
SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

# Socket connection
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(SERVER_ADDR)

print("Connected to the Server\n")
print("*"*29)
print("Welcome to Text Editor Client")
print("*"*29 + "\n")
print("Authanticate First to Continue Application")
print("Please use \"USER\" and \"PASS\" commands\n")

statement = ""
command = ""
response = ""
is_auth = False

while command != "EXIT" and "Exiting" not in response:
    statement = input("Enter request: ")
    command = statement.split(" ", 1)[0]
    statement += NEWLINE
    client_socket.sendall(statement.encode())

    response = client_socket.recv(1024).decode()
    print("\n" + response + "\n")
    
client_socket.close()
print("\n" + "*"*29)
print("End of the Text Editor Client")
print("\tGood Bye")
print("*"*29 + "\n")