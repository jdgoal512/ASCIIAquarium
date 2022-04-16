import json
from typing import List

class Species:
    """Species of fish.

    Has the art and traits associated with the species of fish.

    Attributes:
        name: The species name
        hunger_time: Time in seconds the species would starve if it has not
                     been fed during that time.
        art: List of ascii art strings from youngest to oldest
        art_ages: List of time in seconds for the fish of the given age to
                  progress to the next ascii art.
    """
    def __init__(self, name: str, hunger_time: float, art: List[str], art_ages: List[float]):
        self.name = name
        self.hunger_time = hunger_time
        self.art = art
        self.art_ages = art_ages

    def get_art(self, age) -> str:
        """Returns ascii art for the species at the given age."""
        age_index = 0
        for i in self.art_ages:
            if age < i:
                break
            age_index += 1
        return self.art[age_index]

    def to_json(self) -> str:
        """Returns the name of the species."""
        return self.name

def get_species(filename='data/species.json') -> List[Species]:
    """Read in species from a json file

    Args:
        filename: The filename to read the species from

    Returns:
        List of species read in from the file
    """
    with open(filename) as json_file:
        json_species = json.load(json_file)
        all_s = {}
        for s_name, s_data in json_species.items():
            all_s[s_name] = Species(name=s_name,
                                    hunger_time=s_data['hunger_time'],
                                    art=s_data['art'],
                                    art_ages=s_data['art_ages'])
        return all_s

def main():
    """Print the name of all species read from the file"""
    all_s = get_species('../../data/species.json')
    for species_name in all_s:
        print(species_name)

if __name__ == '__main__':
    main()
