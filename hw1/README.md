# CSE 310 Programming Assignment #1
# By Michael Lee ID: 112424954

## Libraries
The Libraries used for webserver includes socket and requests. The requests library must be installed using package manager pip.

```bash
python -m pip install requests
```

```python
from socket import *
import requests
```

The Libraries used for proxy server includes socket, requests, urlib.request, os, threading

```python
import socket
import requests
from urllib.request import Request, urlopen, HTTPError
import os
import threading
```
## Instructions
To run webserver.py (tested in Chrome), from the hw directory in terminal, type python webserver.py. 

```bash
python webserver.py
```
The address is set at localhost and the port number is 5050. Go to Chrome browser and enter "localhost:5050/HelloWorld.html" to view HelloWorld.html. Enter and other path to receive an 404 Error. 

To run proxyserver.py (tested in Chrome), from the hw directory in terminal, type python proxyserver.py

```bash
python proxyserver.py
```
The address is set at local host and the port number is 5051. Go to Chrome browser and enter "localhost:5051/[url for proxy server to access]. All cached files will be saved in the "cache" directory. 

## Websites Tested
The proxyserver.py has been tested on:
http://gaia.cs.umass.edu/pearson.png
http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html
http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html
