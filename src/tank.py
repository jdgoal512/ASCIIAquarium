import json

from src.fish.fish import Fish
from src.fish.fish_builder import FishBuilder


class Tank:
    def __init__(self, width=30, height=10):
        self.width = width
        self.height = height
        self.fish = []
        self.fish_builder = FishBuilder()

    def add_fish(self, fish: Fish):
        self.fish += [fish]

    def feed(self):
        for f in self.fish:
            f.feed()

    def print(self):
        # TODO: Add drawing of tank with fish
        # print("+" + '=' * self.width + '+')
        # for _ in range(self.height):
        #     print("|" + ' ' * self.width + '|')
        # print("+" + '-' * self.width + '+')
        for i, fish in enumerate(self.fish):
            print(f'{i+1}. {fish.get_status()}')

    def to_json(self):
        text = '{'
        text += f'"width": {self.width},'
        text += f'"height": {self.height}'
        text += '}'
        tank_json = json.loads(text)
        tank_json["fish"] = [f.to_json() for f in self.fish]
        return tank_json

    def load_json(self, tank_json):
        self.width = tank_json["width"]
        self.height = tank_json["height"]
        self.fish = []
        for json_fish in tank_json["fish"]:
            self.add_fish(self.fish_builder.from_json(json_fish))

    def save(self, filename):
        json_text = json.dumps(self.to_json(), indent=4)
        with open(filename, 'w') as save_file:
            save_file.write(json_text)
