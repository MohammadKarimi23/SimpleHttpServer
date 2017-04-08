#!/usr/bin/python

import socket
import sys , getopt

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
                    parseMessage(data)
                    print >>sys.stderr, 'sending data back to the client'
#               connection.sendall(data)
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
        finally:
            connection.close()

def parseMessage(msg):
    print '\nparsing message\n'
    lines = msg.split("\n")
    print lines[0].split(" ")[1]

if __name__ == '__main__':
#    main(sys.argv[1:])
    server(1242)
