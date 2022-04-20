import json
import random
from typing import List


class Personality:
    """Personality of a fish.

    Has quotes for when a fish of the given personality is happy, normal,
    stressed, and is hungry.

    Attributes:
        name: Name of the personality.
        happy_quotes: List of quotes for when it has very low stress.
        normal_quotes: List of quotes for when it as moderately low stress.
        unhappy_quotes: List of quotes for when it has high stress.
        hungry_quotes: List of quotes for when it is hungry.
    """
    def __init__(self, name: str, happy_quotes, normal_quotes, unhappy_quotes, hungry_quotes):
        self.name = name
        self.happy_quotes = happy_quotes
        self.normal_quotes = normal_quotes
        self.unhappy_quotes = unhappy_quotes
        self.hungry_quotes = hungry_quotes

    def get_quote(self, name, stress, hunger):
        """Gets a random quote based on the fish's personality.

        Args:
            stress: Float with fish's stress level, 0 being no stress.
            hunger: Float with fish's hunger level, 0 being completely full.

        Returns:
            String with a quote based on how the fish is feeling.
        """
        possible_quotes = []
        if stress < 0.20:
            possible_quotes += self.happy_quotes
        elif stress < 0.4:
            possible_quotes += self.normal_quotes
        else:
            possible_quotes += self.unhappy_quotes
        if hunger > 0.4:
            possible_quotes += self.hungry_quotes
        quote = random.choice(possible_quotes)
        return quote.replace("{name}", name)

    def to_json(self):
        """Returns the name of the personality"""
        return self.name


def get_personalities(filename='data/personalities.json') -> List[Personality]:
    """Reads in a list of personalities from a file

    Args:
        filename: Filename to read the personalities from.

    Returns:
        List of personalities read in from the json file.
    """
    with open(filename) as json_file:
        json_personalities = json.load(json_file)
        all_p = {}
        for p_name, p_data in json_personalities.items():
            all_p[p_name] = Personality(name=p_name,
                                        happy_quotes=p_data['happy_quotes'],
                                        normal_quotes=p_data['normal_quotes'],
                                        unhappy_quotes=p_data['unhappy_quotes'],
                                        hungry_quotes=p_data['hungry_quotes'])
        return all_p


def main():
    """Prints all the personalities read in from the file"""
    all_p = get_personalities('../../data/personalities.json')
    for p_name, p in all_p.items():
        print(f'### {p_name} ###')
        print('Happy:')
        for _ in range(3):
            print(p.get_quote(name=f'{p_name} Fish', stress=0, hunger=0))
        print('Normal:')
        for _ in range(3):
            print(p.get_quote(name=f'{p_name} Fish', stress=0.3, hunger=0))
        print('Unhappy:')
        for _ in range(3):
            print(p.get_quote(name=f'{p_name} Fish', stress=1, hunger=0))
        print('Hungry:')
        for _ in range(3):
            print(p.get_quote(name=f'{p_name} Fish', stress=0.3, hunger=1))


if __name__ == '__main__':
    main()
