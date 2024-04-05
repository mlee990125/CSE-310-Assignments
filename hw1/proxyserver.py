"""
    Implements a simple cache proxy
"""

import socket
import requests
from urllib.request import Request, urlopen, HTTPError
import os
import threading





def fetch_from_server(filename, url):
  response = requests.get(url)
  if(response.status_code == 404):
    return None
  open("cache/" + filename , "wb").write(response.content)
  return (response.content)

  
def fetch_from_cache(filename):
    try:
        f = open("cache/" + filename, 'rb')
        content = f.read()
        return content
    except IOError:
        return None

def fetch_file(filename, url):
    # Check file locally first
    file_from_cache = fetch_from_cache(filename)

    # If file exists, return. Else fetch from server
    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache
    else:
        print('Not in cache. Fetching from server.')
        file_from_server = fetch_from_server(filename, url)

        if file_from_server:
            return file_from_server
        else:
            return None

# Threading
def handleClient(client_connection, client_address):
  # Get the client request, get the url.
  request = client_connection.recv(4096).decode()
  url = request.split()[1][1:]
  
  # Get file name from url
  filename = os.path.basename(url)
  
  if filename == '/':
      filename = '/index.html'

  # Get the file
  content = fetch_file(filename, url=url)

  # If we have the file, return it, otherwise 404
  if content:
      client_connection.send(("HTTP/1.1 200 OK\r\n\r\n").encode('utf-8'))
      client_connection.send((content))
      
  else:
      client_connection.send(("HTTP/1.1 404 Not Found\r\n\r\n").encode())
      client_connection.send(("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n").encode())
  # Send the response and close the connection
  client_connection.close()

def main():
    # Get port command line argument

    # Define socket host and port
    SERVER_HOST = 'localhost'
    SERVER_PORT = 5051

    # Initialize socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen()

    print('Cache proxy is listening on port %s ...' % SERVER_PORT)

    while True:
        # Wait for client connection
        client_connection, client_address = server_socket.accept()
        thread = threading.Thread(target=handleClient, args=(client_connection, client_address))
        thread.start()

    # Close socket
    server_socket.close()


main()

