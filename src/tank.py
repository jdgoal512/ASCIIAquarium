"""The tank for the aquarium

This holds all the fish and is used to interact with them, like feeding.
The Tank class also holds all relevant data and functions for
the main save file.
"""
import json
import random
from typing import List

from src.fish_art import FishArt
from src.fish.fish import Fish
from src.fish.fish_builder import FishBuilder


class Tank:
    """Tank for the aquarium.

    Attributes:
        width: Width of the interior of the tank in characters.
        height: Height of the interior of the tank in characters.
        max_fish: The maximum number of fish you can put in the tank
        fish: List of fish in the tank.
        fish_builder: Creates fish that are read in from json.
    """
    def __init__(self, width: int = 30, height: int = 10, max_fish: int = 10):
        self.width = width
        self.height = height
        self.max_fish = max_fish
        self.fish = []
        self.art = []
        self.fish_builder = FishBuilder()

    def add_fish(self, fish: Fish):
        """Adds a fish to the tank as long as there is still room in the tank.

        Args:
            fish: The fish to be added.
        """
        if not self.is_full():
            self.fish += [fish]
            x = random.randint(1, self.width - len(fish.get_art()))
            y = random.randint(1, self.height)
            self.art += [FishArt(fish, x, y)]

    def remove_fish(self, fish_name: str):
        """Remove fish with given name from the tank."""
        for fish_art in self.art:
            if fish_art.fish.name == fish_name:
                self.art.remove(fish_art)
                break
        for fish in self.fish:
            if fish.name == fish_name:
                self.fish.remove(fish)
                return f'Goodbye {fish_name}'
        return 'Error, could not remove {fish_name}'


    def feed(self):
        """Feed all fish in the tank."""
        for f in self.fish:
            f.feed()

    def move_fish(self, refresh_rate: float = 1):
        """Randomly move the fish.

        Args:
            refresh_rate: How many times this is called per second.
        """
        for fish in self.art:
            random_movement = random.random()
            if random_movement < 0.2*refresh_rate:  # Flip the fish
                fish.flip()
            elif random_movement < 0.3*refresh_rate: # Move up
                if fish.y > 1:
                    fish.update_position(fish.x, fish.y - 1)
                else:  # Bounce off top of tank
                    fish.update_position(fish.x, fish.y + 1)
            elif random_movement < 0.4*refresh_rate: # Move down
                if fish.y <= self.height:
                    fish.update_position(fish.x, fish.y + 1)
                else:  # Bounce off bottom of tank
                    fish.update_position(fish.x, fish.y - 1)
            elif random_movement < 0.8*refresh_rate: # Move forward
                if fish.flipped:
                    if fish.x <= self.width - len(fish.get_art()):  # Move right
                        fish.update_position(fish.x + 1, fish.y)
                    else:  # Bounce off side of tank
                        fish.flip()
                else:
                    if fish.x > 1:  # Move left
                        fish.update_position(fish.x - 1, fish.y)
                    else:  # Bounce off side of tank
                        fish.flip()


    def draw_tank(self, interval: float = 1) -> List[str]:
        """Create ascii art of the tank with all the fish inside.

        Args:
            interval: How many times this is called per second.

        Returns:
            A list of strings with the ascii art for the tank.
        """
        tank_text = ["+" + '=' * self.width + '+']
        tank_text += ["|" + '~' * self.width + '|']
        for _ in range(self.height):
            tank_text += ["|" + ' ' * self.width + '|']
        tank_text += ["+" + '#' * self.width + '+']
        self.move_fish(interval)

        for fish in self.art:
            fish_art = fish.get_art()
            tank_text[fish.y] = tank_text[fish.y][:fish.x] + fish_art \
                                + tank_text[fish.y][fish.x + len(fish_art):]

        return tank_text

    def is_full(self):
        """Returns whether or not the tank is full."""
        return len(self.fish) >= self.max_fish

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
