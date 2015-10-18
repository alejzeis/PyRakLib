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
import time
import math


class PyRakLib:
    __metaclass__ = ABCMeta

    VERSION = "0.8.0"
    LIBRARY_VERSION = "1.1"
    MAGIC = bytearray("\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78", "UTF-8")

    PRIORITY_NORMAL = 0
    PRIORITY_IMMEDIATE = 1

    FLAG_NEED_ACK = 0b00001000

    """
      Internal Packet:
      int32 (length without this field)
      byte (packet ID)
      payload
    """

    """
      ENCAPSULATED payload:
      byte (identifier length)
      byte[] (identifier)
      byte (flags, last 3 bits, priority)
      payload (binary internal EncapsulatedPacket)
    """
    PACKET_ENCAPSULATED = 0x01
    """
      OPEN_SESSION payload:
      byte (identifier length)
      byte[] (identifier)
      byte (address length)
      byte[] (address)
      short (port)
      long (clientID)
     """
    PACKET_OPEN_SESSION = 0x02
    """
      CLOSE_SESSION payload:
      byte (identifier length)
      byte[] (identifier)
      string (reason)
     """
    PACKET_CLOSE_SESSION = 0x03
    """
      INVALID_SESSION payload:
      byte (identifier length)
      byte[] (identifier)
     """
    PACKET_INVALID_SESSION = 0x04
    """ TODO: implement this
      SEND_QUEUE payload:
      byte (identifier length)
      byte[] (identifier)
     """
    PACKET_SEND_QUEUE = 0x05
    """
      ACK_NOTIFICATION payload:
      byte (identifier length)
      byte[] (identifier)
      int (identifierACK)
     """
    PACKET_ACK_NOTIFICATION = 0x06
    """
      SET_OPTION payload:
      byte (option name length)
      byte[] (option name)
      byte[] (option value)
     """
    PACKET_SET_OPTION = 0x07
    """
      RAW payload:
      byte (address length)
      byte[] (address from/to)
      short (port)
      byte[] (payload)
     """
    PACKET_RAW = 0x08
    """
      RAW payload:
      byte (address length)
      byte[] (address)
      int (timeout)
     """
    PACKET_BLOCK_ADDRESS = 0x09
    """
      No payload
     
      Sends the disconnect message, removes sessions correctly, closes sockets.
     """
    PACKET_SHUTDOWN = 0x7e
    """
      No payload
     
      Leaves everything as-is and halts, other Threads can be in a post-crash condition.
     """
    PACKET_EMERGENCY_SHUTDOWN = 0x7f


def substr(s, start: int, length: int = None):
    """
    Returns the portion of string specified by the start and length
    parameters. Originally from: http://www.php2python.com/wiki/function.substr/
    """
    if len(s) >= start:
        if start > 0:
            return False
        else:
            return s[start:]
    if not length:
        return s[start:]
    elif length > 0:
        return s[start:start + length]
    else:
        return s[start:length]


def microtime(get_as_float: bool = False) -> float:
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())
