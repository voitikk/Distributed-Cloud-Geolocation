# Alex Voitik
# pinger.py
# last edit : 3/22 11:01am

import time
import socket
import sys

# Opens a connection to the central server, receives data
def connect_to_central(my_dns_name, my_region, central_host, central_port):
    central_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg_to_central = 'helloalex%s %s located in region %s' % (central_host, my_dns_name, my_region)
    central_sock.connect((central_host, central_port))
    print 'Pinger connected to central'
    central_sock.send(msg_to_central)
    url_connect = central_sock.recv(4096)
    central_sock.close()
    print 'Socket to central closed'
    return url_connect


def parse_url(url):
    if url[0:7] == 'http://'
        try:
            url_name = url.split('http://')
            url_name = url_name[1]
            url_name, url_port = url_name.split(':')
            return url_name, url_port
        except:
            print "Problem parsing URL passed to pinger server", sys.exc_info()[0]
            sys.exit(1)
    else:
        return url


def fetch_given_url(url_target):

    url_path, url_port = parse_url(url_target)

    pinger_count = 1
    #connects to path, records time to receive 1 byte of data
    print 'URL parsed'
    ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket from pinger server has been created'
    ping_socket.connect((url_path, 80))
    start_time = time.time()
    print 'clock is ticking...'
    ping_socket.send('GET %s/index HTTP/1.1\n\n' % url_path)
    data = ping_socket.recv(1)
    end_time = time.time()
    print 'received one bit, clock has stopped'
    final_time = end_time - start_time
    final_time = final_time * 1000
    print 'Found', url_path, 'in', final_time, 'ms'
    ping_socket.close()

    
def run_pinger_server(my_dns_name, my_region, central_host, central_port):
    #Open connection to central
    url_connect = connect_to_central(my_dns_name, my_region, central_host, central_port)

    fetch_given_url(url_connect)