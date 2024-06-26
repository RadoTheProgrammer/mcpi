import socket
import select
import sys
from .util import flatten_parameters_to_string
from mcpi.timer import t
""" @author: Aron Nieminen, Mojang AB"""

class RequestError(Exception):
    pass

class Connection:
    """Connection to a Minecraft Pi game"""
    RequestFailed = "Fail"
    
    verbose_mode = False
    no_refresh = False
    no_refresh_cmd = ""
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.lastSent = ""

    def drain(self):
        """Drains the socket of incoming data"""
        while True:
            readable, _, _ = select.select([self.socket], [], [], 0.0)
            if not readable:
                break
            data = self.socket.recv(1500)
            e =  "Drained Data: <%s>\n"%data.strip()
            e += "Last Message: <%s>\n"%self.lastSent.strip()
            sys.stderr.write(e)

    def send(self, f, *data):
        """
        Sends data. Note that a trailing newline '\n' is added here

        The protocol uses CP437 encoding - https://en.wikipedia.org/wiki/Code_page_437
        which is mildly distressing as it can't encode all of Unicode.
        """
        p=flatten_parameters_to_string(data)
        #t.print("flattened parameters")
        s = f"{f}({p})\n"
        #t.print("generated command")
        self._send(s)
        #t.print("sent command")

    def _send(self, s):
        """
        The actual socket interaction from self.send, extracted for easier mocking
        and testing
        """
        if self.no_refresh:
            self.no_refresh_cmd += s
        else:
            s = s.encode()
            if self.verbose_mode:print(s)
            self.drain()
            self.lastSent = s

            self.socket.sendall(s)

    def receive(self):
        """Receives data. Note that the trailing newline '\n' is trimmed"""
        s = self.socket.makefile("r")
        t.print("makefile")
        s=s.readline() #TODO this is the line who slow
        t.print("readline")
        s=s.rstrip("\n")
        if s == Connection.RequestFailed:
            raise RequestError("%s failed"%self.lastSent.strip())
        return s

    def sendReceive(self, *data):
        """Sends and receive data"""
        self.send(*data)
        t.print("send")
        return self.receive()
    
    def __enter__(self):
        self.no_refresh_cmd = ""
        self.no_refresh = True
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.no_refresh = False
        self._send(self.no_refresh_cmd)
