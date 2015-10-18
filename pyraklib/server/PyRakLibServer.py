"""
   PyRakLib networking library.
   This software is not affiliated with RakNet or Jenkins Software LLC.
   This software is a port of PocketMine/RakLib <https://github.com/PocketMine/RakLib>.
   All credit goes to the PocketMine Project (http://pocketmine.net)
 
   PyRakLib is free software: you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   PyRakLib is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.
 
  You should have received a copy of the GNU Lesser General Public License
  along with PyRakLib.  If not, see <http://www.gnu.org/licenses/>.
"""
from threading import Thread
from logging import Logger
import queue, atexit
from pyraklib.server import UDPServerSocket
from pyraklib.server.SessionManager import SessionManager


class PyRakLibServer(Thread):

    """@:type int"""
    port = None
    """@:type str"""
    interface = None
    """@:type logging.Logger"""
    logger = None

    """@:type bool"""
    _shutdown = False

    """@:type queue.LifoQueue"""
    internalQueue = None
    """@:type queue.LifoQueue"""
    externalQueue = None

    def __init__(self, logger: Logger, port: int, interface: str):
        super().__init__()
        self.port = port
        self.logger = logger
        if port < 1 or port > 65536:
            raise ValueError("Port is invalid! Must be between 1 and 65536")

        self.interface = interface

        self.internalQueue = queue.LifoQueue()
        self.externalQueue = queue.LifoQueue()

        self.start()

    def is_shutdown(self) -> bool:
        return self._shutdown

    def shutdown(self):
        self._shutdown = True

    def push_main_to_thread_packet(self, packet: bytearray):
        self.internalQueue.put(packet)

    def read_main_to_thread_packet(self) -> bytearray:
        if not self.internalQueue.empty():
            return self.internalQueue.get()
        return None

    def push_thread_to_main_packet(self, packet: bytearray):
        self.externalQueue.put(packet)

    def read_thread_to_main_packet(self) -> bytearray:
        if not self.externalQueue.empty():
            return self.externalQueue.get()
        return None

    def shutdown_handler(self):
        if not self.is_shutdown():
            self.logger.critical("PyRakLib Crashed!")

    def run(self):
        atexit.register(self.shutdown_handler)
        socket = UDPServerSocket(self.logger, self.port, self.interface)

        manager = SessionManager(self, socket)