# Alex Voitik
# central.py

import os        # for os.path.isfile()
import socket    # for socket stuff
import sys       # for sys.argv
import mimetypes # to find file postfixes
import time      # packet time formatting
import urllib    # for parsing urls

host = ""
conn_list = []
conn = None
ping_serv_count = 0
ping_info = []
cent_host_info = ''

# open the files needed
result = open('result.html')
result_file = result.read()
result.close()

index = open('index.html')
index_file = index.read()
print index_file
index.close()


def run_central_coordinator(my_ipaddr, my_zone, my_region, central_host, central_port):
    print 'Running Central Coordinator'
    global ping_serv_count, conn, conn_list, ping_info, host, cent_host_info
    cent_host_info = 'IP: %s Zone: %s Region: %s' % (my_ipaddr, my_zone, my_region)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('', central_port))
        print 'Listening on port', central_port
        s.listen(5)
    except socket.error, msg:
        print "Failed. Error code " + str(msg[0]) + " : " + msg[1]
        sys.exit(1)
    while 1:
        print "Waiting for connection..."
        conn, addr = s.accept()
        print "Connected with " + addr[0] + ":" + str(addr[1])

        # read socket
        try:
            parse = conn.recv(4096)
        except Exception as e:
            print 'Oops, an error happened: ', e
            sys.exit(1)

        if parse[0:9] == 'helloalex':
            print 'hello request from pinger server'
            conn_ip = parse[9:]
            ping_info.append(conn_ip)
            conn_list.append(conn)
            print 'IP of pinger added to connection list'
            print 'There are', len(conn_list), 'pinger servers active'
            ping_serv_count = str(len(conn_list))
        else:
            send_mess, send_data = handle_request(parse)
            conn.send(send_mess)
            conn.send(send_data)
            print 'Message Sent. Waiting for new connection.....\n'


def handle_request(parse):
    parse_split = parse.splitlines()[0]
    further_parse = str(parse_split).split()
    print 'Further Parse : ', further_parse[1]

    # If a URL is being requested
    if further_parse[1] == '/' or further_parse[1] == '/index.html':
        try:
            print 'Opening ' + further_parse[1]
            file = open('index.html')
        except Exception as e:
            print 'index.html not found'
            sys.exit(1)

        data = file.read()
        info_index = data
        info_index = info_index.replace('REPLACE_CONNECTION_STATUS', cent_host_info)
        info_index = info_index.replace('REPLACE_PINGER_NUMBER', ping_serv_count)
        for y in ping_info:
            info_index = info_index.replace('</pre>', y + '\n' + '</pre>')

        currTime = time.ctime()

        cont_type = 'Content-Type: ' + 'text/html' + '\r\n\r\n'
        ok_str = 'HTTP/1.1 200 OK\r\n'
        date = 'Date: ' + currTime + '\r\n'
        server = 'Server: central (ajvoit17)\r\n'
        content_len = 'Content-Length: ' + str(len(info_index)) + '\r\n'
        connection = 'Connection: close\r\n'

        message = ok_str + date + server + content_len + connection + cont_type

        html_code = info_index + '\r\n'

        return message, html_code
    #
    elif further_parse[1][0:11] == '/geolocate?':
        print further_parse[1][0:11]
        print 'Geolocation requested'
        geolocate_results = []
        requested_loc = urllib.unquote(further_parse[1][18:])
        print 'Sending URL to pingers...'
        try:
            print 'Opening geolocate'

            file = open('geolocate.html')
        except Exception as e:
            print 'geolocate.html not found'
            sys.exit(1)

        geoloc_file = file.read()
        for sendconn in conn_list:
            sendconn.send(requested_loc)
        print 'Waiting for responses'

        for recconn in conn_list:
            rec_data = recconn.recv(500)
            geolocate_results.append(rec_data)

        print 'Recieved Data: ', geolocate_results
        geoloc_file = geoloc_file.replace('CONNECTION', host)
        for data in geolocate_results:
            geoloc_file = geoloc_file.replace('</pre>', data + '\n' + '</pre>')

            currTime = time.ctime()

            cont_type = 'Content-Type: text/html\r\n\r\n'
            ok_str = 'HTTP/1.1 200 OK\r\n'
            date = 'Date: ' + currTime + '\r\n'
            server = 'Server: central (ajvoit17)\r\n'
            content_len = 'Content-Length: ' + str(len(geoloc_file)) + '\r\n'
            connection = 'Connection: close\r\n'

            message = ok_str + date + server + content_len + connection + cont_type

            html_code = geoloc_file + '\r\n'

            return message, html_code
    else:
        file_path = further_parse[1]
        if file_path[1:] == 'favicon.ico':
            file_path = file_path[1:]
        if os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            print 'File "%s" Exists!' % file_path[1:]
            content = open(file_path, 'rb').read()

            currTime = time.ctime()

            cont_type = 'Content-Type: ' + content_type + '\r\n\r\n'
            ok_str = 'HTTP/1.1 200 OK\r\n'
            date = 'Date: ' + currTime + '\r\n'
            server = 'Server: central (ajvoit17)\r\n'
            content_len = 'Content-Length: ' + str(len(content)) + '\r\n'
            connection = 'Connection: close\r\n'

            message = ok_str + date + server + content_len + connection + cont_type

            html_code = content + '\r\n'

            return message, html_code
        else:
            print 'Error! File "%s" Does Not Exist!' % file_path[1:]
            return 'HTTP/1.1 404 NOT FOUND', 'NONE'