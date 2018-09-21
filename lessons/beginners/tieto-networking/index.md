## Network Programming

### A socket module

The Python interface is a straightforward transliteration of the Unix system call and library interface for sockets to Python’s object-oriented style: the socket() function returns a socket object whose methods implement the various socket system calls.

Sockets come in two varieties: server sockets and client sockets . After you create a server socket, you tell it to wait for connections. It will then listen at a certain network address (a combination of an IP address and a port number) until a client socket connects. The two can then communicate.

It is instantiated with up to three parameters: an address family (defaulting to socket.AF_INET), whether it’s a stream (socket.SOCK_STREAM, the default) or a datagram (socket.SOCK_DGRAM) socket, and a protocol.

**Minimal server**

```
import socket

s = socket.socket()

host = socket.gethostname()
port = 1234
s.bind((host, port))

s.listen(5)
while True:

    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(b'Thank you for connecting')
    c.close()
```

**Minimal client**

```
import socket

s = socket.socket()

host = socket.gethostname()
port = 1234

s.connect((host, port))
print(s.recv(1024))
```

More informations about socket programming is on [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html).

### The urllib and urllib2 modules

**Opening remote files**

```
from urllib.request import urlopen
webpage = urlopen('http://www.python.org')
```

 the variable webpage should now contain a file-like object linked to the Python web page.
 
**Retreiving remote files**

The urlopen function gives you a file-like object you can read from. If you would rather have urllib take care of downloading the file for you, storing a copy in a local file, you can use urlretrieve instead.

```
from urllib.request import urlretrieve
urlretrieve('http://www.python.org', 'python_webpage.html')
```

**Other important modules**

|  Module | Description  |
|---|---|
|  asynchat |  Additional functionality for asyncore |
|  asyncore | Asynchronous socket handler  |
|  cgi |  Basic CGI support |
| Cookie  | Cookie object manipulation, mainly for servers  |
| cookielib  |  Client-side cookie support |
| email  |  Support for e-mail messages (including MIME) |
| ftplib  |  FTP client module |
| gopherlib  |  Gopher client module |
|  httplib |HTTP client module|
|  imaplib |IMAP4 client module|
|  mailbox | Reads several mailbox formats  |
|  mailcap |  Access to MIME configuration through mailcap files |
|  nntplib |NNTP client module|
|poplib|  POP client module |
|robotparser| Support for parsing web server robot files|
|SimpleXMLRPCServer| A simple XML-RPC server|
| smtpd| SMTP server module|
|smtplib| SMTP client module|
| telnetlib| Telnet client module|
| urlparse| Support for interpreting URLs|
| xmlrpclib| Client support for XML-RPC |

### Simple TCP server and client

```
#!/usr/bin/env python3
# Simple TCP client and server that send and receive 16 octets

import argparse, socket

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())
        message = recvall(sc, 16)
        print('  Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print('  Reply sent, socket closed')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
```

You can try instead of argparse other command line parse modules:

* Docopt (pip install docopt)
* Click (pip install click)
* Invoke (pip install invoke)

### RPC

Remote Procedure Call (RPC) systems let you call a function in another process or on a remote server using the same syntax you would use when calling a routine in a local API or library. This is usefull in situations like:

* Your program has a lot of work to do, and you want to spread it across several machines by making calls across the network, but without having to change the code that is making the call, which is now remote.
* You need data or information that is only available on another hard drive or network, and an RPC interface lets you easily send queries to another system to get back an answer.


### XML-RPC

XML-RPC is a convinient way to send messages across the Internet.

The nice thing about XML-RPC is that it transports native data structures- you can ship off lists, strings, dictionaries, and numbers.

**Server**

```
from xmlrpc.server import SimpleXMLRPCServer

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x // y

# A simple server with simple arithmetic functions
server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_multicall_functions()
server.register_function(add, 'add')
server.register_function(subtract, 'subtract')
server.register_function(multiply, 'multiply')
server.register_function(divide, 'divide')
server.serve_forever()
```

**Client**

List available methods:

```
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
multicall = xmlrpc.client.MultiCall(proxy)
multicall.add(7, 3)
multicall.subtract(7, 3)
multicall.multiply(7, 3)
multicall.divide(7, 3)
result = multicall()

print("7+3=%d, 7-3=%d, 7*3=%d, 7//3=%d" % tuple(result))
```

