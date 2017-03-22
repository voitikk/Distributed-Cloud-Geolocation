# smartsocket.py module
# Author: K. Walsh <kwalsh@cs.holycross.edu>
# Date: 15 January 2015

"""
This module contains the SmartSocket wrapper class that makes sockets a little easier to use.

When reading from a socket, it is nice to be able to read a specific amount (say, up to the first blank line, or a
specific number of bytes). But the regular socket.recv(n) function reads "up to" n bytes. The SmartSocket class is a
simple wrapper around a regular Socket that adds a little extra functionality to make reading easier.

Example usage:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (host, port)
    s.connect(addr)
    s = SmartSocket(s)
    request = s.recv_until("\r\n\r\n")    # This reads everything up to the first blank line
    n = get_content_length_from_http_request(request)
    body = s.recv_exactly(n)              # This reads exactly n bytes, no more, no less
    s.close()
"""

import socket    # for socket stuff

"""SmartSocket wrapper class."""
class SmartSocket():

    """Initialize a new SmartSocket, given a plain Socket s."""
    def __init__(self, s):
        self.s = s
        self.recvd = ""

    """Close the underlying socket."""
    def close(self):
        self.s.close()

    """Get the peer name from the underlying socket."""
    def getpeername(self):
        return self.s.getpeername()

    """Send to the underlyuing socket"""
    def sendall(self, msg):
        return self.s.sendall(msg)

    """
    Receive exactly n bytes, no more, no less, from the underlying socket. Actually, this may read more than n, but any
    extra will be stripped off and saved for subsequent recv calls. This returns the n-byte string, or None if there was
    an error before n-bytes could be received.
    """
    def recv_exactly(self, n):
        while len(self.recvd) < n:
            more = self.s.recv(max(4096, n - len(self.recvd)))
            if not more:
                return None
            self.recvd += more
        msg, self.recvd = self.recvd[0:n], self.recvd[n:]
        return str(msg)

    """
    Receive all bytes up to and including a delimiter of your choice. For example, recv_until("A") will read and return
    all bytes up to and including the first "A". Similarly, recv_until("\r\n") will read and return all bytes up to and
    including the first http-style newline, and recv_until("\r\n\r\n") will read and return everything up to the first
    http-style blank line. This returns the desired string, or None if there was an error before the delimiter was seen.
    """
    def recv_until(self, delim):
        while delim not in self.recvd:
            more = self.s.recv(4096)
            if not more:
                return None
            self.recvd += more
        n = self.recvd.find(delim) + len(delim)
        msg, self.recvd = self.recvd[0:n], self.recvd[n:]
        return str(msg)


