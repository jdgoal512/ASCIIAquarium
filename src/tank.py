"""The tank for the aquarium

This holds all the fish and is used to interact with them, like feeding.
The Tank class also holds all relevant data and functions for
the main save file.
"""
import json
import time

from src.fish.fish import Fish
from src.fish.fish_builder import FishBuilder


DAY = 60*60*24
DEFAULT_WIDTH = 30
DEFAULT_HEIGHT = 10
DEFAULT_MAX_FISH = 10


class Tank:
    """Tank for the aquarium.

    Attributes:
        width: Width of the interior of the tank in characters.
        height: Height of the interior of the tank in characters.
        max_fish: The maximum number of fish you can put in the tank
        waste: Amount of waste in the tank.
        fish: List of fish in the tank.
        fish_builder: Creates fish that are read in from json.
        last_checkin: Timestamp of when the stress was last updated.
    """
    def __init__(self,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT,
                 max_fish: int = DEFAULT_MAX_FISH,
                 waste: float = 0,
                 last_checkin: float = None):
        self.width = width
        self.height = height
        self.max_fish = max_fish
        self.waste = waste
        self.fish = []
        self.fish_builder = FishBuilder()
        if last_checkin is not None:
            self.last_checkin = last_checkin
        else:
            self.last_checkin = time.time()

    def add_fish(self, fish: Fish):
        """Adds a fish to the tank as long as there is still room in the tank.

        Args:
            fish: The fish to be added.
        """
        if not self.is_full():
            self.fish += [fish]

    def remove_fish(self, fish_name: str):
        """Remove fish with given name from the tank."""
        for fish in self.fish:
            if fish.name == fish_name:
                self.fish.remove(fish)
                return f'Goodbye {fish_name}'
        return f'Error, could not remove {fish_name}'

    def feed(self):
        """Feed all fish in the tank."""
        self.checkin()
        for f in self.fish:
            f.feed()

    def clean(self):
        """Clean the tank if there is a significant amount of waste."""
        if self.waste > 0.15:
            self.waste = 0
            self.checkin()
            return "The tank is squeaky clean now"
        self.checkin()
        return "The tank is still pretty clean"

    def checkin(self, timestamp: float = None):
        """Update the amount of waste and checkin on the waste.

        Updates the amount of waste based on the number of fish and the
        timestamp for when the last check in occurred. It will recursively
        checkin for each day that has passed since the last checkin.

        Args:
            timestamp: If given, perform the check in as if it were that time.
                       Otherwise check in using the current time.
        """
        if timestamp is None:
            timestamp = time.time()
        # Recursively checkin for each day that has passed
        if self.last_checkin + DAY < timestamp:
            self.checkin(timestamp - DAY)
        for fish in self.fish:
            fish.checkin(timestamp)
        time_delta = timestamp - self.last_checkin
        new_waste = 0.05*time_delta*len(self.fish)/DAY
        self.waste += new_waste
        self.last_checkin = timestamp


    def get_status(self):
        """Get how clean the tank is and how the fish are doing."""
        self.checkin()
        fish_status = [fish.get_status() for fish in self.fish]
        return fish_status

    def is_full(self):
        """Returns whether or not the tank is full."""
        return len(self.fish) >= self.max_fish

    def to_json(self) -> dict:
        """Returns a dict of the tank that can be serialized with json."""
        tank_json = {
            "width": self.width,
            "height": self.height,
            "waste": self.waste
        }
        tank_json["fish"] = [f.to_json() for f in self.fish]
        return tank_json

    def load_json(self, tank_json: dict):
        """Loads data from serialized json into the tank

        Args:
            tank_json: dict with the serialized json of a tank
        """
        self.width = tank_json.get("width", DEFAULT_WIDTH)
        self.height = tank_json.get("height", DEFAULT_HEIGHT)
        self.waste = tank_json.get("waste", 0)
        self.fish = []
        for json_fish in tank_json["fish"]:
            self.add_fish(self.fish_builder.from_json(json_fish))

    def save(self, filename):
        """Save the tank to a file.

        Serializes the tank to json and saves it to a file.

        Args:
            filename: The file to save the tank to.
        """
        self.checkin()
        json_text = json.dumps(self.to_json(), indent=4)
        with open(filename, 'w') as save_file:
            save_file.write(json_text)
