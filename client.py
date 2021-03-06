import socket
import select
import sys
import random
import message
import time

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    print("ex: python3 client.py 127.0.0.1 8080\n")
    exit()

IP_address = str(sys.argv[1])
port = int(sys.argv[2])
UDP_port = 8081 # UDP port fixed
client_id = random.randrange(1000, 4001)
#wait for the client to type "Log on" to be connected
while(sys.stdin.readline() != "Log on\n"):
	{
	}

# create a UDP connection for the intial handshake with server
handshake = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP connection

# send HELLO(clientID_A) message to server using UDP to begin connection
msg = message.make_msg("HELLO", *[str(client_id)])
handshake.sendto(msg.encode(), (IP_address, UDP_port))

handshake.close()

# creates TCP connection with chat server after handshake is complete
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP_address, port))

while True:
    # select() does not work on stdin on windows
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    # receive and display messages, if any. Otherwise, read from stdin
    for socks in read_sockets:
        if socks == server:
            Message = socks.recv(2048)
            server_msg = Message.decode()
            if "CLIENTREQUESTID" == server_msg[:15]:
                print("CHAT_STARTED ")
                j = server_msg[15:] # flag = int(message.decode()[15:])
                server.send(("CLIENTREQUESTID" + j).encode()) # Message.decode()[15:]
            elif "END_NOTIF" in server_msg:
                server.send(("END_NOTIF".encode()))
                print(server_msg)
            elif "End Chat" in server_msg:
                print(server_msg)
            else:
                print(server_msg)
        else:
            Message = sys.stdin.readline()

            server.send(Message.encode())
            sys.stdout.write("<You> ")
            sys.stdout.write(Message)
            sys.stdout.flush()
server.close()
