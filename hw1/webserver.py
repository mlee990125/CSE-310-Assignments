from socket import *
import requests

# Create Server Port
serverPort = 5050
servSock = socket(AF_INET, SOCK_STREAM)
servSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
servSock.bind(("localhost", serverPort))
servSock.listen(1)
FORMAT = 'utf-8'


def start():
  print(f"Listening on localhost:{serverPort}")
  while True:
    connSock, addr = servSock.accept()

    try:
      message = connSock.recv(1024).decode(FORMAT)
      
      # Get File name and open it.
      filename = message.split()[1]
      f = open(filename[1:])
      outputdata = f.read()


      # If successfully opened, send status 200 and the file to client
      connSock.send(("HTTP/1.1 200 OK\r\n\r\n").encode())
      connSock.send((outputdata + '\r\n').encode())

    
      connSock.send(("\r\n").encode())
      connSock.close()

      # Else return a 404 Error
    except IOError:
      connSock.send(("HTTP/1.1 404 Not Found\r\n\r\n").encode())
      connSock.send(("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n").encode())
      connSock.close()


print("The server is starting...")
start()