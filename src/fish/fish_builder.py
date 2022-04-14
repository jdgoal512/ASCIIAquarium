from src.fish.fish import Fish
from src.fish.personality import get_personalities
from src.fish.species import get_species


class FishBuilder:
    """Used to create fish with a given personality and species.

    Attributes:
        personalities: List of personalities the fish could have.
        species: List of species the fish could be.
    """
    def __init__(self, species_file: str = 'data/species.json',
                 personality_file: str = 'data/personalities.json'):
        self.personalities = get_personalities(personality_file)
        self.species = get_species(species_file)

    def get_fish(self, name: str, species_name: str, personality_name: str) -> Fish:
        """Creates a fish.

        Args:
            name: Name for the fish.
            species_name: String with the name of the species for the fish.
            personality_name: Name of the personality for the fish.

        Returns:
            Fish with the given name, species, and personality.
        """
        try:
            personality = self.personalities[personality_name]
        except IndexError:
            raise IndexError(f'Personality {personality_name} not found')
        try:
            species = self.species[species_name]
        except IndexError:
            raise IndexError(f'Species {species_name} not found')
        return Fish(name=name, species=species, personality=personality)

    def from_json(self, fish_json: dict) -> Fish:
        """Recreates a fish from serialized json.

        Args:
            fish_json: Dict with data to rebuild a fish.

        Returns:
            Fish recreated from the serialized json.
        """
        try:
            personality = self.personalities[fish_json["personality"]]
        except IndexError:
            raise IndexError(f'Personality {fish_json["personality"]} not found')
        try:
            species = self.species[fish_json["species"]]
        except IndexError:
            raise IndexError(f'Species {fish_json["species"]} not found')
        return Fish(name=fish_json["name"],
                    species=species,
                    personality=personality,
                    birth=fish_json["birth"],
                    last_fed=fish_json["last_fed"],
                    stress=fish_json["stress"],
                    last_checkin=fish_json["last_checkin"])
