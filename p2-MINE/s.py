import socket
import sys
import time

def parse_url(url):
    try:
        url_name = url.split('http://')
        url_name = url_name[1]
        url_name, url_port = url_name.split(':')
        return url_name, url_port
    except:
        print "Problem parsing URL passed to pinger server", sys.exc_info()[0]
        sys.exit(1)

url = raw_input('Ented a URL: ')
url_path, url_port = parse_url(url_target)
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