import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
history = ""

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        else:

            message = sys.stdin.readline().strip()
            if (message == "/exec"):
                exec(history) 
            server.send(message + "\n")            
            if (message == "/history"):
                print(history)
                server.send(history)
            history += message + "\n"
            if (message == "/clear"):
                history = ""
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.write("\n")
            sys.stdout.flush()
server.close()