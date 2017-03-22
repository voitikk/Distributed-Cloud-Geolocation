# Alex Voitik
# central.py
#last edit: 3/21 12:07

import os        # for os.path.isfile()
import socket    # for socket stuff
import sys       # for sys.argv
import urllib    # for urllib.unquote()()
import time      # for time.time()

#used for local testing, will remove
host = ""
port = 8888
root = "/index.html"
conn_list = []

def handle_request(conn, root):
    parse = conn.recv(4096)
    if not parse:
        print "Empty Request"
        sys.exit(1)
    if parse[0:9] == 'helloalex':
        print 'hello request from pinger server'
        conn_ip = parse[10:]
        conn_list.append(conn_ip)
        print 'IP added to connection list'
        print 'There are', len(conn_list), 'servers active'

    else:
        further_parse = parse.splitlines()[0]
        packet_headers = str(further_parse).split()
        if parse[0:8] == 'FORM_REQ':
            print 'URL Form Request...'
            status = 'HTTP/1.1 200 OK'
            date = time.ctime()
            messg = 'Connection to URL OK'
            mime_type = 'text/plain'
        if packet_headers[1] == '/index.html' or packet_headers[1] == '/':
            print 'Index page requested'
        if packet_headers[1][0:11] == '/geolocate?':
            print 'Geolocate request'


def run_central_coordinator(my_ipaddr, my_zone, my_region, central_host, central_port):
    print 'Running Central Coordinator'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, central_port))
        print 'Document Root is'  + root
        print 'Listening on port', port
        s.listen(1)
    except socket.error, msg:
        print "Failed. Error code " + str(msg[0]) + " : " + msg[1]
        sys.exit(1)
    while 1:
        print "Waiting for connection"
        conn, addr = s.accept()
        print "Connected with " + addr[0] + ":" + str(addr[1])
        handle_request(conn, addr)

            
    