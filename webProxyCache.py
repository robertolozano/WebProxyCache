from socket import *
import sys

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
#Bind to socket and port #
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)
# Fill in end.
refererFlag = 0

while 1:
    # Start receiving data from the client
    print()
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024)  # Fill in start. # Fill in end.
    originalMessage = message
    print(message)

    try:
        #Extract Search Term
        search = message.split()[1]
        print(search)

        #Remove first parantheses from search term
        filename = message.split()[1].partition(b"/")[2]
        hostn = filename.partition(b"/")[0]
        print("hostname:",hostn)
    except:
        continue
    filename = filename.decode('utf-8')

    print("filename:", filename)
    fileExist = "false"
    filetouse = "/" + filename
    print("filetouse:", filetouse)

    if b"Referer" in message:
        refererFlag = 1
        print("REFERER EXISTS")
        print(message.partition(b"Referer: http://localhost:8888")[2])
        message = message.partition(b"Referer: http://localhost:8888")[2]
        print(message.partition(b"/")[2])
        message = message.partition(b"/")[2]
        # filename = message.partition(b"/")[0]
        filename = message.decode()
        print(filename.partition('\r')[0])
        filename = filename.partition('\r')[0]
        hostn = filename.partition('/')[0]
        print("hostname:", hostn)

    try:

        append = originalMessage.split()[1]
        append = append.decode()
        append = append.replace("//","_")
        append = append.replace("/","_")
        filename_temp = filename.replace("/","_")
        filetouse = "/" +filename_temp + append
        print("FILETOUSE:",filetouse)

        # Check whether the file exist in the cache
        f = open(filetouse[1:], "rb")
        print("File exists")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode('utf-8'))
        tcpCliSock.send("Content-Type:text/html\r\n".encode('utf-8'))
        # Fill in start.
        for line in range(len(outputdata)):
            # tcpCliSock.send(outputdata[line].encode('utf-8'))
            tcpCliSock.send(outputdata[line])

        # Fill in end.
        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        print("File doesn't exist")
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)  # Fill in start. # Fill in end.
            # hostn = filename#.replace("www.", "", 1)
            print("hostn:", hostn)

            try:
                # Connect to the socket to port 80
                # hostn = "www.cs.toronto.edu"

                print("connecting to host", hostn)
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client

                # request = "GET "+"http://" + hostn + " HTTP/1.0\r\n\r\n"
                request = "GET "+"http://" + filename + " HTTP/1.0\r\n\r\n"
                print("request:", request)


                if refererFlag == 1:
                    print("Search term:",originalMessage.split()[1])
                    search = originalMessage.split()[1]
                    search = search.decode()
                    if search[0] == "/":
                        request = "GET http://" + search + " HTTP/1.0\r\n\r\n"
                    else:
                        request = "GET http://" + search + " HTTP/1.0\r\n\r\n"
                    print(request)
                    refererFlag = 0


                print("request:", request)
                c.send(request.encode())

                tempMessage = c.recv(1024, MSG_WAITALL)
                totalMessage = tempMessage
                print(tempMessage)
                print("length:", len(tempMessage))

                while len(tempMessage) > 0:
                    tempMessage = c.recv(1024)
                    totalMessage = totalMessage + tempMessage

                tcpCliSock.send(totalMessage)

                #Create a new file in the cache for the requested file.
                #Also send the response in the buffer to client socket and the corresponding file in the cache
                print("before make file")
                append = originalMessage.split()[1]
                append = append.decode()
                append = append.replace("//","_")
                append = append.replace("/","_")
                filename_temp = filename.replace("/","_")
                print("making file:", "x"+filename_temp+append+"x")
                print("after make file")
                tmpFile = open("./" + filename_temp+append, "wb")
                tmpFile.write(totalMessage)
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode('utf-8'))
            tcpCliSock.send("Content-Type:text/html\r\n".encode('utf-8'))
            tcpCliSock.send("\r\n".encode('utf-8'))
# Close the client and the server sockets
tcpCliSock.close()

# # Fill in start.
tcpSerSock.close()
# # Fill in end.
