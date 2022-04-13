#!/usr/bin/env python3
'''
    Virtual Fish Tank
  +==================+
  |                  |
  |-------*---*------|
  |                  |
  |  o/o    <* ><    |
  |  o\o             |
  |   o\o      /|/   |
  |   o/o     \|/    |
  +==================+
'''

import os
import json

from src.fish.fish_builder import FishBuilder
from src.tank import Tank
from src.cmd_interface.interface import Interface

def main():
    filename = 'save.json'
    tank = Tank()
    if os.path.isfile(filename):
        print(f'Loading {filename}')
        with open(filename, 'r') as json_file:
            json_object = json.load(json_file)
        tank.load_json(json_object)
    else:
        print('Creating a new tank')
        builder = FishBuilder()
        tank.add_fish(builder.get_fish('Molly', 'Mosquitofish', 'Energetic'))
        tank.add_fish(builder.get_fish('Bubbles', 'Goldfish', 'Laid Back'))
        tank.add_fish(builder.get_fish('Silver', 'Goldfish', 'Energetic'))
    gui = Interface(tank)
    gui.run()
    tank.save(filename)

if __name__ == '__main__':
    main()
