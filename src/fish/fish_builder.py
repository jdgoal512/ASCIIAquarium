import json

from src.fish.fish import Fish
from src.fish.personality import Personality, get_personalities
from src.fish.species import get_species


class FishBuilder:
    def __init__(self, species_file: str = 'src/fish/species.json',
                 personality_file: str = 'src/fish/personalities.json'):
        self.personalities = get_personalities(personality_file)
        self.species = get_species(species_file)

    def get_fish(self, name, species_name, personality_name):
        try:
            personality = self.personalities[personality_name]
        except IndexError:
            raise IndexError(f'Personality {personality_name} not found')
        try:
            species = self.species[species_name]
        except IndexError:
            raise IndexError(f'Species {species_name} not found')
        return Fish(name=name, species=species, personality=personality)

    def from_json(self, fish_json):
        try:
            personality = self.personalities[fish_json["personality"]]
        except IndexError:
            raise IndexError(f'Personality {personality_name} not found')
        try:
            species = self.species[fish_json["species"]]
        except IndexError:
            raise IndexError(f'Species {species_name} not found')
        return Fish(name=fish_json["name"],
                    species=species,
                    personality=personality,
                    birth=fish_json["birth"],
                    last_fed=fish_json["last_fed"],
                    stress=fish_json["stress"],
                    last_checkin=fish_json["last_checkin"])
