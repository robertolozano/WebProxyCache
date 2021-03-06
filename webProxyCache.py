from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
#Bind to socket and port #
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)
# Fill in end.

while 1:
    # Strat receiving data from the client
    print()
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024)# Fill in start. # Fill in end.
    print(message)

    # Extract the filename from the given message
    # print(message.split()[1])
    filename = message.split()[1].partition(b"/")[2]
    filename = filename.decode('utf-8')

    print("filename:",filename)
    fileExist = "false"
    filetouse = "/" + filename
    print("filetouse:",filetouse)

    # try:
    #     # Check wether the file exist in the cache
    #     f = open(filetouse[1:], "r")
    #     outputdata = f.readlines()
    #     fileExist = "true"
    #     # ProxyServer finds a cache hit and generates a response message
    #     tcpCliSock.send("HTTP/1.0 200 OK\r\n")
    #     tcpCliSock.send("Content-Type:text/html\r\n")
    #     # Fill in start.
    #     for line in range(len(outputdata)):
    #         tcpCliSock.send(outputdata[line])
    #     # Fill in end.
    #     print('Read from cache')

#     # Error handling for file not found in cache
    # except IOError:
    if fileExist == "false":
        # Create a socket on the proxyserver
        c = socket(AF_INET, SOCK_STREAM)# Fill in start. # Fill in end.
        hostn = filename.replace("www.","",1)
        print("hostn:",hostn)

        try:
            # Connect to the socket to port 80
            # Fill in start.
            c.connect((hostn, 80))
            # Fill in end.
            # Create a temporary file on this socket and ask port 80 for the file requested by the client

            request = "GET "+"http://" + hostn + " HTTP/1.0\r\n\r\n"


            if "css" in filename:
                cssPath = filename
                print("found css")
                filename = message.partition(b"Referer:")[2]

                print(filename)
                filename = message.partition(b"Referer:")[2].partition(b"www.")
                print("1:",filename)
                filename = filename[1] + filename[2]
                print("2:",filename)
                filename = filename.partition(b"\r")[0]
                print("PATH:",filename + filetouse.encode())
                filename = filename + filetouse.encode()
                filename = filename.decode("utf-8")
                request = "GET "+"http://" + hostn + " HTTP/1.0\r\n\r\n"



            print("request:", request)
            c.send(request.encode())

            tempMessage = c.recv(1024, MSG_WAITALL)
            totalMessage = tempMessage
            print(tempMessage)
            print("length:",len(tempMessage))

            while len(tempMessage) > 0:
                tempMessage = c.recv(1024)
                totalMessage = totalMessage + tempMessage

            tcpCliSock.send(totalMessage)

            # print()
            # tempMessage = tcpCliSock.recv(1024)
            # print(tempMessage)

            # Read the response into buffer

            # Fill in start.
            # Fill in end.

            # Create a new file in the cache for the requested file.
            # Also send the response in the buffer to client socket and the corresponding file in the cache
            # tmpFile = open("./" + filename,"wb")

            # Fill in start.
            # for line in fileData:
                # tmpFile.write(line)
                # tcpCliSock.send(line)

            # Fill in end.
        except:
            print("Illegal request")
    else:
        # HTTP response message for file not found
        # Fill in start.
        tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n")                             
        tcpCliSock.send("Content-Type:text/html\r\n")
        tcpCliSock.send("\r\n")
        # Fill in end.
# Close the client and the server sockets
tcpCliSock.close()

# # Fill in start.
tcpSerSock.close()
# # Fill in end.