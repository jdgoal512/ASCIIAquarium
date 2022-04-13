import json

class Species:
    def __init__(self, name: str, hunger_time: float):
        self.name = name
        self.hunger_time = hunger_time

    def to_json(self):
        return self.name

def get_species(filename='species.json'):
    with open(filename) as json_file:
        json_species = json.load(json_file)
        all_s = {}
        for s_name, s_data in json_species.items():
            all_s[s_name] = Species(name=s_name,
                                        hunger_time=s_data['hunger_time'])
        return all_s

def main():
    all_s = get_species()
    for species_name in all_s:
        print(species_name)

if __name__ == '__main__':
    main()
