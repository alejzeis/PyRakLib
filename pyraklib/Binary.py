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
from abc import ABCMeta
from struct import pack, unpack


class Binary:
    __metaclass__ = ABCMeta

    BIG_ENDIAN = 0x00
    LITTLE_ENDIAN = 0x01

    @staticmethod
    def read_l_triad(data: bytes):
        return unpack('<i', data + b'\x00')[0]

    @staticmethod
    def write_l_triad(triad: int) -> bytes:
        return pack('<i', triad)[:3]

    @staticmethod
    def read_byte(raw: bytes, signed: bool =True) -> int:
        if signed:
            return unpack('>b', raw)[0]
        else:
            return unpack('>B', raw)[0]

    @staticmethod
    def write_byte(byte: int, signed: bool = True) -> bytes:
        if signed:
            return pack(">b", byte)
        else:
            return pack(">B", byte)

    @staticmethod
    def read_short(raw: bytes) -> int:
        return unpack(">H", raw)[0]

    @staticmethod
    def read_signed_short(raw: bytes) -> int:
        return unpack(">h", raw)[0]

    @staticmethod
    def write_short(short: int) -> bytes:
        return pack(">H", short)

    @staticmethod
    def read_int(raw: bytes) -> int:
        return unpack(">i", raw)[0]

    @staticmethod
    def write_int(i: int) -> bytes:
        return pack(">i", i)

    @staticmethod
    def read_float(raw: bytes) -> float:
        return unpack(">f", raw)[0]

    @staticmethod
    def write_float(f: float) -> float:
        return pack(">f", f)

    @staticmethod
    def read_double(raw: bytes) -> float:
        return unpack(">d", raw)[0]

    @staticmethod
    def write_double(d: float) -> bytes:
        return pack(">d", d)

    @staticmethod
    def read_long(raw: bytes) -> int:
        return unpack(">q", raw)[0]

    @staticmethod
    def write_long(l: int) -> bytes:
        return pack(">q", l)
