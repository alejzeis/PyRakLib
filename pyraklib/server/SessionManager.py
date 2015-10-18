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
import copy
import logging
from pyraklib import PyRakLib
from pyraklib.protocol import *
from pyraklib.server import UDPServerSocket
from pyraklib.PyRakLib import microtime
from pyraklib.server import PyRakLibServer
import random, sys, time


class SessionManager:
    packet_pool = {}

    """@:type PyRakLibServer"""
    server = None
    """@:type UDPServerSocket"""
    socket = None

    """@:type int"""
    _recieveBytes = 0
    """@:type int"""
    _sendBytes = 0

    """@:type int"""
    _serverId = 0

    sessions = {}

    """@:type str"""
    name = ""

    """@:type int"""
    _packetLimit = 1000

    """@:type bool"""
    shutdown = False

    """@:type int"""
    ticks = 0
    """@:type int"""
    last_measure = None

    block = {}
    ipSec = {}

    port_checking = True

    def __init__(self, server: PyRakLibServer, socket: UDPServerSocket):
        self.server = server
        self.socket = socket
        self._register_packets()

        self._serverId = random.randint(0, sys.maxsize)

        self.run()

    def get_logger(self) -> logging.Logger:
        return self.server.logger

    def run(self):
        self._tick_processor()

    def _tick_processor(self):
        self.last_measure = microtime(True)
        while not self.shutdown:
            start = microtime(True)
            max = 5000
            while self._receive_packet():
                max -= 1
            while self._receive_stream():
                pass

            t = microtime(True) - start
            if t < 0.05:
                time.sleep((microtime(True) + 0.05 - t) - time.time())
            self._tick()

    def _tick(self):
        pass


    def _receive_packet(self) -> bool:
        data = self.socket.read_packet()
        if data is not None and len(data[0]) > 0:
            buffer = data[0]
            ip = data[1][0]
            port = data[1][1]
            address = ip+":"+str(port)
            self._recieveBytes += len(buffer)
            if address in self.block:
                return True

            if address in self.ipSec:
                self.ipSec[address] += 1
            else:
                self.ipSec[address] = 1

            pid = buffer[0]
            packet = self.get_packet_from_pool(pid)
            if packet is not None:
                packet.buffer = buffer
                if isinstance(packet, UNCONNECTED_PING) or isinstance(packet, UNCONNECTED_PING_OPEN_CONNECTIONS):
                    # No need to create a session for just pings
                    packet.decode()
                    pk = UNCONNECTED_PONG()
                    pk.serverID = self._serverId
                    pk.pingID = packet.pingID
                    pk.serverName = self.name
                    self.send_packet(pk, ip, port)
                    return True
                else:
                    self.get_session(ip, port).handle_packet(packet)
                    return True
            else:
                # self.stream_raw()
                return True

        return False

    def send_packet(self, packet: Packet, ip: str, port: int):
        packet.encode()
        self._sendBytes += len(packet.buffer)
        self.socket.write_packet(packet.buffer, ip, port)

    def stream_encapsulated(self, session, packet: EncapsulatedPacket, flags: int = PyRakLib.PRIORITY_NORMAL):
        pass

    def _receive_stream(self) -> bool:
        packet = self.server.read_main_to_thread_packet()
        if packet is not None:
            return True
        return False

    def block_address(self, address: str, timeout: int = 300):
        final = microtime(True) + timeout
        if address not in self.block or timeout == -1:
            if timeout == -1:
                final = sys.maxsize
            else:
                self.get_logger().info("Blocked "+address+" for "+str(timeout)+" seconds.")
            self.block[address] = final
        elif self.block[address] < final:
            self.block[address] = final

    def _register_packet(self, id: int, clazz):
        self.packet_pool[id] = clazz()

    def get_packet_from_pool(self, id: int) -> Packet:
        try:
            return copy.copy(self.packet_pool[id])
        except:
            return None

    def _register_packets(self):
        self._register_packet(UNCONNECTED_PING.get_pid(None), UNCONNECTED_PING)
        self._register_packet(UNCONNECTED_PING_OPEN_CONNECTIONS.get_pid(None), UNCONNECTED_PING_OPEN_CONNECTIONS)
        self._register_packet(UNCONNECTED_PONG.get_pid(None), UNCONNECTED_PONG)