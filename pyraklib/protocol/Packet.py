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
from abc import ABCMeta, abstractmethod
from pyraklib import Binary
from pyraklib.PyRakLib import substr


class Packet:
    __metaclass__ = ABCMeta

    """@:type int"""
    _offset = 0
    """@:type bytearray"""
    buffer = None
    """@:type int"""
    sendTime = None

    def get(self, length) -> bytes:
        if length < 0:
            self._offset = len(self.buffer) - 1

            return None
        elif length:
            return substr(self.buffer, self._offset)

        buffer = bytearray()
        while length > 0:
            length -= 1
            self._offset += 1
            buffer.append(self.buffer[self._offset])

        return buffer

    def get_long(self) -> int:
        return Binary.read_long(self.get(8))

    def get_int(self) -> int:
        return Binary.read_int(self.get(4))

    def get_short(self, signed: bool = True) -> int:
        if signed:
            return Binary.read_signed_short(self.get(2))
        else:
            return Binary.read_short(self.get(2))

    def get_l_triad(self) -> int:
        return Binary.read_l_triad(self.get(3))

    def get_byte(self) -> int:
        return self.get(1)

    def get_string(self) -> str:
        return self.get(self.get_short(False)).decode("UTF-8")

    """
    Return is in format: ([ip version (usually 4)], [ip address], [port]
    """
    def get_address(self) -> tuple:
        version = self.get_byte()
        if version == 4:
            addr = str(((~self.get_byte()) & 0xff)) +"."+ str(((~self.get_byte()) & 0xff)) +"."+ str(((~self.get_byte()) & 0xff)) +"."+ str(((~self.get_byte()) & 0xff))
            port = self.get_short(False)
            return (version, addr, port)
        else:
            # TODO: IPv6
            pass
        return None

    def feof(self) -> bool:
        try:
            self.buffer[self._offset]
            return False
        except IndexError:
            return True

    def put(self, data: bytes):
        self.buffer.append(data)

    def put_long(self, l: int):
        self.buffer.append(Binary.write_long(l))

    def put_int(self, i: int):
        self.buffer.append(Binary.write_int(i))

    def put_short(self, s: int):
        self.buffer.append(Binary.write_short(s))

    def put_l_triad(self, t: int):
        self.buffer.append(Binary.write_l_triad(t))

    def put_byte(self, b: int, signed: bool = False):
        self.buffer.append(Binary.write_byte(b, signed))

    def put_string(self, s: str):
        self.put_short(len(s))
        self.put(bytes(s, "UTF-8"))

    def put_address(self, addr: str, port: int, version: int):
        self.put_byte(version)
        if version == 4:
            for b in addr.split("."):
                self.put_byte((~(int(b))) & 0xff)
            self.put_short(port)
        else:
            # TODO: IPv6
            pass

    def encode(self):
        self.put_byte(self.get_pid())

    def decode(self):
        self._offset = 1

    def clean(self):
        self.buffer = bytearray()
        self._offset = 0
        self.sendTime = None
        return self

    @abstractmethod
    def get_pid(self) -> int: pass