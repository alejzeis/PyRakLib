"""
PyRakLib networking library.
   This software is not affiliated with RakNet or Jenkins Software LLC.
   This software is a port of PocketMine/RakLib <https://github.com/PocketMine/RakLib>.
   All credit goes to the PocketMine Project (http://pocketmine.net)
 
   Copyright (C) 2015  PyRakLib Project

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os, logging
import atexit
from threading import Thread
from pyraklib.Queue import Queue
from pyraklib.server.SessionManager import SessionManager
from pyraklib.server.UDPServerSocket import UDPServerSocket


class PyRakLibServer(Thread):
    port = None
    interface = None

    logger = None
    loadPaths = []

    _shutdown = False

    externalQueue = []
    internalQueue = []

    mainPath = None

    def __init__(self, port, logger = logging.getLogger("PyRakLib"),interface = "0.0.0.0"):

        super().__init__()
        self.port = port
        if port < 1 or port > 65536:
            raise Exception("Invalid port range")

        self.interface = interface
        self.logger = logger
        self.mainPath = os.getcwd()

        self.internalQueue = Queue()
        self.externalQueue = Queue()

        self.start()

    def shutdown(self):
        self._shutdown = True

    def shutdownHandler(self):
        if self._shutdown is not True:
            self.logger.error("PyRakLib Thread [#"+str(self.ident)+"] crashed.")

    def pushMainToThreadPacket(self, pkt):
        self.internalQueue.append(pkt)

    def readMainToThreadPacket(self):
        return self.internalQueue.shift()

    def pushThreadToMainPacket(self, pkt):
        self.externalQueue.append(pkt)

    def readThreadToMainPacket(self):
        return self.externalQueue.shift()

    def run(self):
        atexit.register(self.shutdownHandler)

        socket = UDPServerSocket(self.logger, self.port, self.interface)
        SessionManager(self, socket)