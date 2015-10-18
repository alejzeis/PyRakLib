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
import math
from pyraklib import Binary
from pyraklib.PyRakLib import substr


class EncapsulatedPacket:
    reliability = None
    has_split = False
    length = 0
    message_index = None
    order_index = None
    order_channel = None
    split_count = None
    split_id = None
    split_index = None
    buffer = None
    need_ack = False
    identifier_ack = None

    @staticmethod
    def from_binary(binary: bytearray, internal: bool = False, offset: int = None) -> tuple:
        packet = EncapsulatedPacket()

        flags = binary[0]
        packet.reliability = reliability = (flags & 0b11100000) >> 5
        packet.has_split = has_split = (flags & 0b00010000) > 0
        if internal:
            length = Binary.read_int(substr(binary, 1, 4))
            packet.identifier_ack = Binary.read_int(substr(binary, 5, 4))
            offset = 9
        else:
            length = int(math.ceil(Binary.read_short(substr(binary, 1, 2)) / 8))
            offset = 3
            packet.identifier_ack = None

        if reliability > 0:
            if reliability >= 2 and reliability != 5:
                packet.message_index = Binary.read_l_triad(substr(binary, offset, 3))
                offset += 3
            if reliability <= 4 and reliability != 2:
                packet.order_index = Binary.read_l_triad(substr(binary, offset, 3))
                offset += 3
                packet.order_channel = binary[offset]
                offset += 1

        if has_split:
            packet.split_count = Binary.read_int(substr(binary, offset, 4))
            offset += 4
            packet.split_id = Binary.read_short(substr(binary, offset, 2))
            offset += 2
            packet.split_index = Binary.read_int(substr(binary, offset, 4))
            offset += 4

        packet.buffer = substr(binary, offset, length)
        offset += length

        return offset, packet

    def __len__(self) -> int:
        l = 3 + len(self.buffer)
        if self.message_index is not None:
            l += 3
        if self.order_channel is not None:
            l += 4
        if self.has_split:
            l += 10
        return l

    def get_total_length(self) -> int:
        return len(self)

    def to_binary(self, internal: bool = False) -> bytearray:
        binary = bytearray()
        if self.has_split:
            binary.append((self.reliability << 5) | (self.has_split & 0b00010000))
        else:
            binary.append((self.reliability << 5) | (0))

        if internal:
            binary.append(Binary.write_int(len(self.buffer)))
            binary.append(Binary.write_int(self.identifier_ack))
        else:
            binary.append(Binary.write_short(len(self.buffer) << 3))

        if self.reliability > 0:
            if self.reliability >= 2 and self.reliability != 5:
                binary.append(Binary.write_l_triad(self.message_index))
            if self.reliability <= 4 and self.reliability != 2:
                binary.append(Binary.write_l_triad(self.order_index))
                binary.append(Binary.write_byte(self.order_channel))

        if self.has_split:
            binary.append(Binary.write_int(self.split_count))
            binary.append(Binary.write_short(self.split_id))
            binary.append(Binary.write_int(self.split_index))

        binary.append(self.buffer)
        return binary

    def __str__(self):
        return self.to_binary()