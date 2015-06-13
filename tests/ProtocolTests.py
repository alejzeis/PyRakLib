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
from pyraklib.protocol import *
from pyraklib.protocol import __all__
import sys

print("PyRakLib protocol class test script.\nTesting "+str(len(__all__)) + " packets.")

goodTests = 0
failedTests = 0
try:
    ack = ACK()
    ack.seqNums = [1, 2, 3, 4, 5, 8, 22]
    ack.encode()
    if ack.buffer[0] is not ack.getPID():
        raise Exception("Buffer PID is not equal to Packet PID.")
    ack.decode()
    print("ACK Test succeeded")
    goodTests += 1

except Exception as e:
    print("ACK Encode failed: " + str(e))
    failedTests += 1

try:
    nack = NACK()
    nack.seqNums = [1, 2, 3, 4, 5, 8, 22]
    nack.encode()
    if nack.buffer[0] is not nack.getPID():
        raise Exception("Buffer PID is not equal to Packet PID. Comparison: "+str(nack.buffer[0]) + " != " + str(nack.getPID()))
    nack.decode()
    print("NACK Test succeeded")
    goodTests += 1

except Exception as e:
    print("NACK Encode failed: " + str(e))
    failedTests += 1

try:
    pkt = ADVERTISE_SYSTEM()
    pkt.pingID = 123
    pkt.serverID = 1234
    pkt.serverName = "MCPE;HI THERE"
    pkt.encode()
    if pkt.buffer[0] is not pkt.PID:
        raise Exception("Buffer PID is not equal to Packet PID.")
    pkt.decode()
    print("ADVERTISE_SYSTEM succeeded")
    goodTests += 1

except Exception as e:
    print("ADVERTIZE_SYSTEM Encode failed: " + str(e))
    failedTests += 1

try:
    pkt = UNCONNECTED_PONG()
    pkt.pingID = 123
    pkt.serverID = 1234
    pkt.serverName = "MCPE;HI THERE"
    pkt.encode()
    if pkt.buffer[0] is not pkt.PID:
        raise Exception("Buffer PID is not equal to Packet PID.")
    pkt.decode()
    print("UNCONNECTED_PONG succeeded")
    goodTests += 1

except Exception as e:
    print("UNCONNECTED_PONG Encode/Decode failed: " + str(e))
    failedTests += 1



print("Succeeded tests: " + str(goodTests) + "\nFailedTests: "+str(failedTests))
print(type(ord("\x7f")))
if failedTests is not 0:
    sys.exit(1)
else:
    sys.exit(0)