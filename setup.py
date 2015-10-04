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
from setuptools import setup, find_packages
from pyraklib import PyRakLib

setup(
    name="PyRakLib",
    version=PyRakLib.LIBRARY_VERSION,
    description="A port of the PHP RakLib library to Python.",
    long_description="PyRakLib is a networking library that follows the RakNet protocol for MCPE. It is ported from the PHP library: RakLib.\nYou can find the original library here: https://github.com/PocketMine/RakLib",
    url="https://github.com/jython234/PyRakLib",
    author="jython234",
    author_email="jython234@gmail.com",
    license="LGPL V3",
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='PHP library MCPE minecraft raknet raklib networking Python',
    packages=find_packages(where='.', exclude=['tests']),
    requires=['requests']
)