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
import socket, logging, sys


class UDPServerSocket:

    _logger = None
    _socket = None

    def __init__(self, logger: logging.Logger, port: int = 19132, interface: str = "0.0.0.0"):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allows sending broadcast messages
        try:
            self._socket.bind((interface, port))
        except socket.error as e:
            logger.error("*** FAILED TO BIND TO "+interface+":"+str(port)+"!")
            logger.error("Perhaps another server is already running on that port?")
            sys.exit(1)
        finally:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setblocking(False)

    def close(self):
        self._socket.close()

    def read_packet(self) -> tuple:
        data = None
        try:
            data = self._socket.recvfrom(65535)
        except BlockingIOError:
            pass
        finally:
            return data

    def write_packet(self, buffer: bytearray, dest: str, port: int) -> bool:
        return self._socket.sendto(buffer, (dest, port))