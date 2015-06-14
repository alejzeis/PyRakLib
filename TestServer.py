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
from pyraklib.server import PyRakLibServer
from pyraklib.server import ServerHandler
import time
import sys

try:
    server = PyRakLibServer(19132)
    handler = ServerHandler(server, None)
    handler.sendOption("name", "MCCPP;MINECON;TestServer")

    time.sleep(10)
    handler.shutdown()
    time.sleep(2)
    sys.exit(0)
except Exception as e:
    server.logger.critical("Test Failed: "+str(e))
    sys.exit(1)