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
from abc import ABCMeta, abstractmethod
from pyraklib.Binary import Binary


class Packet:
    __metaclass__ = ABCMeta
    offset = 0
    buffer = bytearray()
    sendTime = None

    def get(self, length = 1):
        if length < 0:
            offset = len(self.buffer) - 1

            return ""
        elif isinstance(length, bool) and length:
            return self.buffer[0:self.offset]
        else:
            buffer = self.buffer[self.offset:self.offset+length]
            self.offset += length
            return buffer

    def getLong(self):
        return Binary.readLong(self.get(8))

    def getInt(self):
        return Binary.readInt(self.get(4))

    def getShort(self):
        return Binary.readShort(self.get(2))

    def getLTriad(self):
        return Binary.readLTriad(self.get(3))

    def getByte(self):
        return ord(self.get())

    def getString(self):
        return self.get(self.getShort())

    def getAddress(self):
        version = self.getByte()
        if version == 4:
            addr = str(((~self.getByte())) & 0xff) +"."+ str(((~self.getByte() & 0xff))) +"."+ str(((~self.getByte()) & 0xff)) +"." + str(((self.getByte()) & 0xff))
            port = self.getShort()
            return (addr, port, version)

    def feof(self):
        try:
            self.buffer[self.offset]
            return True
        except IndexError:
            return False

    def put(self, data):
        self.buffer += data

    def putByte(self, b, signed = True):
        self.buffer += Binary.writeByte(b, signed)

    def putLong(self, l):
        self.buffer += Binary.writeLong(l)

    def putInt(self, i):
        self.buffer += Binary.writeInt(i)

    def putShort(self, s):
        self.buffer += Binary.writeShort(s)

    def putLTriad(self, t):
        self.buffer += Binary.writeLTriad(t)

    def putAddress(self, addr, port, version = 4):
        self.putByte(version)
        if version == 4:
            for s in str(addr).split("."):
                self.putByte(int(s) & 0xff, False)
            self.putShort(port)

    def putString(self, string):
        self.buffer += Binary.writeShort(len(string))
        self.buffer += bytes(string, "UTF-8")

    def clean(self):
        self.buffer = bytearray()
        self.offset = 0
        self.sendTime = None

    def cleanBuffer(self):
        self.buffer = bytearray()
        self.offset = 0
        self.sendTime = None

    def encode(self):
        self.cleanBuffer()
        self._encode()

    def decode(self):
        self.offset = 0
        self._decode()

    @abstractmethod
    def _encode(self): pass

    @abstractmethod
    def _decode(self): pass