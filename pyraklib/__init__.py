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
import warnings, sys
from pyraklib.PyRakLib import PyRakLib
# Check dependencies
try:
    import requests
    canCheck = True
except ImportError:
    warnings.warn("Could not import library \"requests\", can not check for latest version.")
    canCheck = False

if sys.version_info[0] < 3:
    print("[CRITICAL]: Requires Python >= 3")
    sys.exit(1)

if canCheck:
    r = requests.get("https://pypi.python.org/pypi/PyRakLib/json")
    v = r.json()['info']['version']
    if v != PyRakLib.LIBRARY_VERSION:
        warnings.warn("You are not using the latest version of PyRakLib: The latest version is: "+v+", while you have: "+PyRakLib.LIBRARY_VERSION)

__all__ = ['PyRakLib', 'Binary']

from pyraklib.Binary import Binary
from pyraklib.PyRakLib import PyRakLib
