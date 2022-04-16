#!/usr/bin/env python3
"""
     Ascii Aquarium
  +==================+
  |                  |
  |-------*---*------|
  |                  |
  |  o/o    <* ><    |
  |  o\o             |
  |   o\o      /|/   |
  |   o/o     \|/    |
  +==================+

Feed your fish every day to make sure they are happy and grow.
"""

import os
import json

from src.tank import Tank
#from src.cmd_interface.interface import Interface
from src.urwid_interface.interface import Interface

def main():
    """Open up the aquarium"""
    # Get OS dependant save file location
    if 'APPDATA' in os.environ:
        config_folder = os.environ['APPDATA']
    elif 'XDG_CONFIG_HOME' in os.environ:
        config_folder = os.environ['XDG_CONFIG_HOME']
    else:
        config_folder = os.path.join(os.environ['HOME'], '.config')
    filename = os.path.join(config_folder, 'afish')

    tank = Tank()
    if os.path.isfile(filename):
        with open(filename, 'r') as json_file:
            json_object = json.load(json_file)
        tank.load_json(json_object)
    else:
        print('Creating a new tank')
    gui = Interface(tank)
    gui.run()
    tank.save(filename)

if __name__ == '__main__':
    main()
