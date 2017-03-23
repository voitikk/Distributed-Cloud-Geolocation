# Alex Voitik
# pinger.py
# last edit : 3/22

import time
import socket
import random


# Opens a connection to the central server, receives data
def run_pinger_server(my_dns_name, my_ipaddr, my_region, central_host, central_port):

    # Open socket to central
    print 'Opening socket to central from pinger'
    central_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg_to_central = 'helloalex%s %s located in %s region' % (my_ipaddr, my_dns_name, my_region)

    # Attempt to connect to the host
    while 1:
        try:
            central_sock.connect((central_host, central_port))
            print 'Pinger connected to central'
            central_sock.send(msg_to_central)
            break
        except Exception as e:
            # If failed, try again in 2 seconds
            time.sleep(2)

    while 1:
        target_url = central_sock.recv(4096)

        # Take out the http:// in the url string
        if target_url[0:7] == 'http://':
            target_url = target_url[7:]

        collection_of_rtt_times = []

        for rtt_ct in range(6):
            # connects to path, records time to receive 1 byte of data
            ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print 'Socket from pinger server has been created'
            ping_socket.connect((target_url, 80))
            start_time = time.time()
            print 'clock is ticking...'
            ping_socket.send('GET %s/index.html HTTP/1.1\n\n' % target_url)
            data = ping_socket.recv(1)
            end_time = time.time()
            print 'received one bit, clock has stopped'
            final_time = end_time - start_time
            print 'Found', target_url, 'in', final_time, 'ms'
            collection_of_rtt_times.append(final_time)
            time.sleep(random.uniform(0.25, 1.0))

        # Find the minimum RTT from the list
        minimum_rtt = min(collection_of_rtt_times)
        central_information = 'URL: %s / Location: %s / RTT Time: %s' % (target_url, my_region, minimum_rtt)
        central_sock.send(central_information)
