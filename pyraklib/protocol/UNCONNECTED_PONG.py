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
from pyraklib import PyRakLib
from pyraklib.protocol import Packet


class UNCONNECTED_PONG(Packet):

    """@:type int"""
    pingID = None
    """@:type int"""
    serverID = None
    """@:type str"""
    serverName = None

    def encode(self):
        super().encode()
        self.put_long(self.pingID)
        self.put_long(self.serverID)
        self.put(PyRakLib.MAGIC)
        self.put_string(self.serverName)

    def decode(self):
        super().decode()
        self.pingID = self.get_long()
        self.serverID = self.get_long()
        self._offset += 16
        self.serverName = self.get_string()

    @staticmethod
    def get_pid(self) -> int:
        return 0x1C
