"""The tank for the aquarium

This holds all the fish and is used to interact with them, like feeding.
The Tank class also holds all relevant data and functions for
the main save file.
"""
import json
import random
from typing import List

from src.fish.fish import Fish
from src.fish.fish_builder import FishBuilder

def _double_replace(text: str, char1: str, char2: str) -> str:
    """Swaps instances of char1 and char2 in a string.

    Args:
        text: The text to do the replacements in.
        char1: One of the strings to swap.
        char2: The other of the strings to swap.

    Returns:
        A string with the substrings swapped
    """
    TEMP = '!@#$%^&temp!@#$%&' # Giberish that would never actually show up
    text = text.replace(char1, TEMP)
    text = text.replace(char2, char1)
    text = text.replace(TEMP, char2)
    return text

def _reverse(text: str) -> str:
    """Reverses a line of ascii art.

    Flips directional characters like / and { as well.

    Args:
        text: String containing the ascii art to be flipped.

    Returns:
        String with the text reversed and directional characters replaced
        with their counterparts.
    """
    text = text[::-1]
    text = _double_replace(text, '<', '>')
    text = _double_replace(text, '{', '}')
    text = _double_replace(text, '(', ')')
    text = _double_replace(text, '[', ']')
    text = _double_replace(text, '/', '\\')
    return text

class Tank:
    """Tank for the aquarium.

    Attributes:
        width: Width of the interior of the tank in characters.
        height: Height of the interior of the tank in characters.
        fish: List of fish in the tank.
        fish_builder: Creates fish that are read in from json.
    """
    def __init__(self, width: int = 30, height: int = 10):
        self.width = width
        self.height = height
        self.fish = []
        self.fish_builder = FishBuilder()

    def add_fish(self, fish: Fish):
        """Adds a fish to the tank.

        Args:
            fish: The fish to be added
        """
        self.fish += [fish]

    def feed(self):
        """Feed all fish in the tank"""
        for f in self.fish:
            f.feed()

    def draw_tank(self) -> List[str]:
        """Create ascii art of the tank with all the fish inside.

        Returns:
            A list of strings with the ascii art for the tank
        """
        tank_text = ["+" + '=' * self.width + '+']
        tank_text += ["|" + '~' * self.width + '|']
        for _ in range(self.height):
            tank_text += ["|" + ' ' * self.width + '|']
        tank_text += ["+" + '#' * self.width + '+']

        for fish in self.fish:
            fish_art = fish.get_art()
            # Randomly flip fish
            if random.random() > 0.5:
                fish_art = _reverse(fish_art)
            fish_x = random.randint(1, self.width - len(fish_art))
            fish_y = random.randint(1, self.height)
            tank_text[fish_y] = tank_text[fish_y][:fish_x] + fish_art \
                                + tank_text[fish_y][fish_x + len(fish_art):]

        return tank_text


    def print(self):
        """Print ascii art of the tank and fish status."""
        for line in self.draw_tank():
            print(line)
        for i, fish in enumerate(self.fish):
            print(f'{i+1}. {fish.get_status()}')
        if not self.fish:
            print('The tank is empty.')

    def to_json(self) -> dict:
        """Returns a dict of the tank that can be serialized with json."""
        tank_json = {
            "width": self.width,
            "height": self.height
        }
        tank_json["fish"] = [f.to_json() for f in self.fish]
        return tank_json

    def load_json(self, tank_json: dict):
        """Loads data from serialized json into the tank

        Args:
            tank_json: dict with the serialized json of a tank
        """
        self.width = tank_json["width"]
        self.height = tank_json["height"]
        self.fish = []
        for json_fish in tank_json["fish"]:
            self.add_fish(self.fish_builder.from_json(json_fish))

    def save(self, filename):
        """Save the tank to a file.

        Serializes the tank to json and saves it to a file.

        Args:
            filename: The file to save the tank to.
        """
        json_text = json.dumps(self.to_json(), indent=4)
        with open(filename, 'w') as save_file:
            save_file.write(json_text)
