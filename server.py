#!/usr/bin/python

import socket
import sys , getopt
import os.path
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

#def main(argv):
#    port = ''
#    try: 
#        opts, args = getopt(argv,"hp:",["port="])
#    except getopt.GetoptError:
#        print 'server.py -p <portnumber>'
#        sys.exit(2)
#    for opt, arg in opts:
#        if opt == '-h':
#            print 'server.py -p <portNumber>'
#            sys.exit()
#        elif opt in ("-p","--port"):
#            port = arg
#    print 'port numm is "', port
#     server(int(port))


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', port)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    sock.listen(1)

    while True:
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        try:
            print >>sys.stderr, 'connection from', client_address
            while True:
                data = connection.recv(1024)
#                parseMessage(data)
         #       print >>sys.stderr, 'received'
         #       print >>sys.stderr, '"%s"' % data
                if data:
                    uri = parseMessage(data)
                    resp = createResponse(uri)
                    print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(resp)
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
        finally:
            connection.close()

def parseMessage(msg):
    print '\nparsing message\n'
    lines = msg.split("\n")
    return lines[0].split(" ")[1]

def createResponse(path):
    Status = ''
    Server = 'Server: Mammads Server (Linux)'
    now = datetime.now()
    stamp = mktime(now.timetuple())
    Date = format_date_time(stamp)
    Connection = 'Connection: Closed'
    response = ''
    Content_type = 'Content-Type: text/html'
    Content_length = ''
    Data = ''
    status_code = 400

    Data, status_code = parsePage(path)
    Content_length = 'Content-Length: ' + str(len(Data))
    if status_code == 200:
        Status = 'HTTP/1.1 200 OK'
    else:
        Status = 'HTTP/1.1 404 Not Found'

    response = Status + '\n\r'
    response += Date + '\n\r'
    response += Server + '\n\r'
    response += Content_length + '\n\r'
    response += Connection + '\n\r'
    response += Content_type + '\n\n'
    response += Data
    return response

def parsePage(path):
    path = "." + path
    res = ''
    code = 0
    if os.path.exists(path):
        code = 200
    else:
        code = 404
        path = "./404.html"
    f = open(path)
    res = f.read()
    return res,code

if __name__ == '__main__':
#    main(sys.argv[1:])
    server(1245)
