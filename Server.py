# -*- coding: utf-8 -*-
import socket
from threading import Thread
import random
import sys
import os

ENCODING = "ascii"
NEWLINE = "\r\n"
USERNAME = "bilkentstu"
PASS = "cs421f2022"

SERVER_SHUTDOWN_MESSAGE = "Server shutdown. Please fix your code according to the response message and retry."


HEADER_SIZE = 2
MAX_DATA_SIZE = 2**(HEADER_SIZE*8) - 1

# Socket stuff
IP = sys.argv[1]
CONTROL_PORT = int(sys.argv[2])


class ServerShutdownException(Exception):
    pass

class VersionConflictException(Exception):
    pass

class VersionMatchException(Exception):
    pass

class InvalidVersionException(Exception):
    pass

class LineMismatchException(Exception):
    pass



class ClientThread(Thread):

    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn
        self.yes_no_flag = False

    def run(self):
        global version
        global file
        try:
            print("Client connected.")

            f = self.conn.makefile(buffering=1, encoding=ENCODING, newline=NEWLINE)

            # Authenticate and get client data port
            check = auth_check(f, self.conn)
            while check == False:
                fail_str = "Authentication Failed\nDo you want to retry? (type \"YES\" or \"NO\")"
                send_response(self.conn, success=False, info=fail_str)
                
                cmd, args = receive_command(f)
                if cmd == "YES":
                    send_response(self.conn, success=True, info="Retrying Credentials...")
                    check = auth_check(f, self.conn)
                else:
                    send_response(self.conn, success=True, info="Exiting...")
                    raise ServerShutdownException
            

            while True:
                cmd, args = receive_command(f)

                if cmd == "APND":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        dissected_args = args.split(" ", 1)
                        try:
                            if len(dissected_args) == 2 and int(dissected_args[0]) == version:
                                append(dissected_args[1], file)
                                version += 1
                                send_response(self.conn, success=True, info = str(version))
                            else:
                                raise VersionConflictException

                        except VersionConflictException:
                            send_response(self.conn, success=False, info=str(version) + " is the current version, please get an update.")

                elif cmd == "WRTE":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        dissected_args = args.split(" ", 2)
                        try:
                            if len(dissected_args) == 3 and int(dissected_args[0]) == version:
                                write(int(dissected_args[1]), dissected_args[2], file)
                                version += 1
                                send_response(self.conn, success=True, info = str(version))
                            else:
                                raise VersionConflictException

                        except VersionConflictException:
                            send_response(self.conn, success=False, info=str(version) + " is the current version, please get an update.")

                        except LineMismatchException:
                            send_response(self.conn, success=False, info= "No such line exists.")

                elif cmd == "DSPLY":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        dissected_args = args.split(" ")
                        try:
                            if len(dissected_args) == 1 and int(dissected_args[0]) == version:
                                result = "\"" + display_file_content(file) + "\""
                                send_response(self.conn, success=True, info = "Displaying the file content\n" + result)
                            else:
                                raise VersionConflictException

                        except VersionConflictException:
                            send_response(self.conn, success=False, info=str(version) + " is the current version, please get an update.")


                elif cmd == "DSPLYLN":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        dissected_args = args.split(" ", 1)
                        try:
                            if len(dissected_args) == 2 and int(dissected_args[0]) == version:
                                result = display_line_content_in_file(file, int(dissected_args[1]))
                                if result is None:
                                    raise LineMismatchException
                                else:
                                    send_response(self.conn, success=True, info = "Displaying the content at line " + dissected_args[1] + "\n" + "\"" + result + "\"")
                            else:
                                raise VersionConflictException

                        except VersionConflictException:
                            send_response(self.conn, success=False, info=str(version) + " is the current version, please get an update.")

                        except LineMismatchException:
                            send_response(self.conn, success=False, info= "No such line exists.")

                elif cmd == "CLR":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        dissected_args = args.split(" ")
                        try:
                            if len(dissected_args) == 1 and int(dissected_args[0]) == version:
                                clear_content(file)
                                version += 1
                                send_response(self.conn, success=True, info = str(version) + ". Content of the file is cleared.")
                            else:
                                raise VersionConflictException

                        except VersionConflictException:
                            send_response(self.conn, success=False, info=str(version) + " is the current version, please get an update.")

                elif cmd == "CLRLN":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        dissected_args = args.split(" ", 1)
                        try:
                            if len(dissected_args) == 2 and int(dissected_args[0]) == version:
                                result = clear_line_content(file, int(dissected_args[1]))
                                if result is False:
                                    raise LineMismatchException
                                else:
                                    version += 1
                                    send_response(self.conn, success=True, info = str(version) + ". The content at line " + dissected_args[1] + " is cleared.")
                            else:
                                raise VersionConflictException

                        except VersionConflictException:
                            send_response(self.conn, success=False, info=str(version) + " is the current version, please get an update.")

                        except LineMismatchException:
                            send_response(self.conn, success=False, info= "No such line exists.")

                elif cmd == "UPDT":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        try:
                            if int(args) != version:
                                content = update(file)
                                send_updt_response(self.conn, success=True, info = str(version), content = content)
                            elif int(args) == version:
                                raise VersionMatchException
                            else:
                                raise InvalidVersionException

                        except VersionMatchException:
                            send_response(self.conn, success=False, info = str(version) + " is already the last version.")

                        except InvalidVersionException:
                            send_response(self.conn, success=False, info = str(version) + " is invalid for Update.")

                elif cmd == "EXIT":
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        send_response(self.conn, success=True, info="Exiting...")
                        break

                elif cmd in ["USER", "PASS"]:
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        response_str = " command is already sent and processed."
                        response_str += "\nTry another command"
                        send_response(self.conn, success=False, info = cmd + response_str)

                elif cmd == "YES":
                    if self.yes_no_flag:
                        self.yes_no_flag = False
                        send_response(self.conn, success=True, info="Proceeding to the application")
                    else:
                        send_response(self.conn, success=False, info="\"YES\" command is not not valid in this context")

                elif cmd == "NO":
                    if self.yes_no_flag:
                        self.yes_no_flag = False
                        send_response(self.conn, success=True, info="Exiting...")
                        break
                    else:
                        send_response(self.conn, success=False, info="\"NO\" command is not not valid in this context")

                else:
                    if self.yes_no_flag:
                        send_response(self.conn, success=False, info = "Use \"YES\" or \"NO\" command")
                    else:
                        response_str = display_exit_or_proceed_menu()
                        self.yes_no_flag = True
                        send_response(self.conn, success=False, info = response_str)

        except ServerShutdownException:
            pass

        except ConnectionResetError as e:
            print(e)

        finally:
            self.conn.close()


#Functions
def send_response(s, success, info=""):
    response = "OK" + " " + info if success else "INVALID " + info
    response = response + "\r\n"
    s.sendall(response.encode())

def send_updt_response(s, success, info="", content = ""):
    response = "OK" + " " + info + " " + content if success else "INVALID " + info
    response = response + "\r\n"
    s.sendall(response.encode())

def receive_command(f):
    line = f.readline()[:-len(NEWLINE)]
    idx = line.find(" ")

    if idx == -1:
        idx = len(line)

    cmd = line[:idx]
    args = line[idx+1:]
    print("Command received:", cmd, args)
    return cmd, args

def shutdown():
    print(SERVER_SHUTDOWN_MESSAGE)
    raise ServerShutdownException

def auth_check(f, conn):

    # Username check
    check = False
    cmd, args = receive_command(f)

    if cmd == "USER":
        if args == USERNAME:
            send_response(conn, success=True)
            check = True
        else:
            send_response(conn, success=False, info="Wrong username.")
    else:
        send_response(conn, success=False, info="Wrong command. Expecting USER.")

    if not check:
        return check

    # Password check
    check = False
    cmd, args = receive_command(f)
    if cmd == "PASS":
        if args == PASS:
            send_response(conn, success=True)
            check = True
        else:
            send_response(conn, success=False, info="Wrong password.")
    else:
        send_response(conn, success=False, info="Wrong command. Expecting PASS.")

    if not check:
        return check

def append(dargs, filepointer):
    filepointer.seek(0,2)
    filepointer.write(dargs + "\n")
    filepointer.flush()

def write(linenum, arg, filepointer):
    filepointer.seek(0,0)
    linelist = filepointer.readlines()
    if linenum - 1 not in range(len(linelist)):
        raise LineMismatchException
    filepointer.seek(0,0)
    linelist[linenum - 1] = arg + "\n"
    filepointer.writelines(linelist)
    filepointer.flush()

def update(filepointer):
    filepointer.seek(0,0)
    linelist = filepointer.readlines()
    content = ""
    for i in linelist:
        content = content + i
    return content


# Additional Functions
def display_exit_or_proceed_menu():
    response_str = "Unknown command.\nDo you want to proceed?\n"
    response_str += "Use \"YES\" command to stay in the application\n"
    response_str += "Use \"NO\" command to exit the application"
    return response_str

def display_file_content(f):
    f.seek(0)
    result = f.read()
    f.seek(0)
    return result

def display_line_content_in_file(f, line_no):
    f.seek(0)
    line_list = f.readlines()
    f.seek(0)
    print(line_no)
    print(len(line_list))
    if line_no - 1 in range(len(line_list)):
        return line_list[line_no - 1]
    else:
        return None

def clear_content(f):
    f.seek(0)
    f.truncate()
    f.seek(0)

def clear_line_content(f, line_no):
    f.seek(0)
    line_list = f.readlines()
    f.seek(0)
    if line_no - 1 not in range(len(line_list)):
        return False
    else:
        line_list[line_no - 1] = ""
        f.truncate()
        f.seek(0)
        f.writelines(line_list)
        f.flush()
        return True

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":

    version = 0

    file = open("CS421_2022FALL_PA1.txt","r+")


    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((IP, CONTROL_PORT))
    threads = []

    while True:
        tcpServer.listen(5)
        print ("TextEditor Server : Waiting for connections..." )
        (conn, (ip,port)) = tcpServer.accept()
        newthread = ClientThread(conn)
        newthread.start()
        threads.append(newthread)


    for t in threads:
        t.join()
    tcpServer.close()
    file.close()


