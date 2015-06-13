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
import socket
from struct import pack, unpack
import re
from pyraklib.Binary import Binary

#data = (pack("N", 1)[0:3])
#data = pack('<i', 1)[:3]
#data = data[::-1] #Little endian triad
#print(data)
#print(unpack('>i', b'\x00' + data)[0])
#print(unpack('<i', data + b'\x00')[0])
from pyraklib.protocol.EncapsulatedPacket import EncapsulatedPacket
from pyraklib.protocol.UNCONNECTED_PING import UNCONNECTED_PING
from pyraklib.protocol.UNCONNECTED_PONG import UNCONNECTED_PONG

data = Binary.writeLTriad(32)
print(Binary.readLTriad(data))

data = Binary.writeByte(32)
print(Binary.readByte(data))

data = Binary.writeShort(256)
print(Binary.readShort(data))

data = Binary.writeInt(32)
print(Binary.readInt(data))

data = Binary.writeLong(32)
print(Binary.readLong(data))

data = Binary.writeFloat(32.54)
print(Binary.readFloat(data))

data = Binary.writeDouble(32.3232)
print(Binary.readDouble(data))

print(type(Binary.writeLong(23)))

ping = UNCONNECTED_PING()
ping.pingID = 1234
ping.encode()

p = EncapsulatedPacket()
p.reliability = 2
p.messageIndex = 1

p.buffer = Binary.writeLong(int(900000))

a = 1

data = p.toBinary()
print(data)

split_length = 5
string = "asdfsadf asdfsadf asd fasd fsdf "
result = filter(None, re.split('(.{1,%d})' % split_length, string))
print(result)

"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
s.sendto(ping.buffer, ("54.148.82.188", 19132))

recvData = s.recvfrom(2048)

pong = UNCONNECTED_PONG()
pong.buffer = recvData[0]
pong.decode()

print(pong.serverName)
"""