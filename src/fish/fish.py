import time

from src.fish.species import Species
from src.fish.personality import Personality


class Fish:
    """Fish to put in the aquarium.

    Attributes:
        name: The name of the fish.
        species: The species of the fish.
        personality: The personality of the fish.
        last_fed: Timestamp of when it was last fed.
        birth: Timestamp with when it was first created.
        stress: Float from 0-1 of how stressed the fish is, 0 being no stress.
        last_checkin: Timestamp of when the stress was last updated.
        time_fed: Time in seconds of how long the fish has been fed.
    """
    def __init__(self,
                 name: str,
                 species: Species,
                 personality: Personality,
                 last_fed: float = None,
                 birth: float = None,
                 stress: float = 0.25,
                 last_checkin: float = None,
                 time_fed: float = 0):
        self.name = name
        self.species = species
        self.personality = personality
        self.stress = stress
        self.time_fed = time_fed
        if birth:
            self.birth = birth
        else:
            self.birth = time.time()
        if last_fed:
            self.last_fed = last_fed
        else:
            self.last_fed = time.time() - self.species.hunger_time/3
        if last_checkin:
            self.last_checkin = last_checkin
        else:
            self.last_checkin = time.time()

    def get_status(self) -> str:
        """Gets a summary on the fish's current status.

        Returns:
            String with the fish's name, species, and a quote based on how
            it is feeling
        """
        self.checkin()
        quote = self.personality.get_quote(name=self.name,
                                           stress=self.stress,
                                           hunger=self.get_hunger())
        return f'{self.name} ({self.species.name}): {quote}'

    def get_art(self) -> str:
        """Gets ascii art for the fish

        The art is based on the fish's age and species

        Returns:
            String with ascii art for the fish
        """
        return self.species.get_art(self.time_fed)

    def feed(self):
        """Feed the fish.

        Updates the time since it was last fed if it hasn't eaten recently.
        """
        hunger = (time.time() - self.last_fed)/self.species.hunger_time
        if hunger > 0.2:
            self.last_fed = time.time()

    def get_current_stress(self, timestamp: float = None) -> float:
        """Gets the fish's current stress level

        Stress is based off how long it has been since it has last eaten.

        Args:
            timestamp: If provided, it calculate the fish's stress at the given
                       time. If not provided, it will calculate the stress
                       based off the current time.
       Returns:
           Float between 0 and 1 with the fish's stress level, with 0 being
           no stress.
        """
        if not timestamp:
            timestamp = time.time()

        hunger = self.get_hunger(timestamp)
        hunger = max(0, (hunger - 0.5)/0.5)
        stress = hunger
        return stress

    def checkin(self, timestamp: float = None):
        """Reavaluate the fish's stress and increment the time it has been fed.

        Updates the fish's stress and the timestamp for when the last check in
        occurred. Stress is adjusted based on how long it has been since the
        last check in. If 24 hours have passed since the last check in the old
        and new stress are averaged. Should not be used without a timestamp if
        over 24 hours has passed since the last check in. Instead this should
        be called multiple times with the timestamp for when the check in would
        have occurred every 24 hours.

        Args:
            timestamp: If given, perform the check in as if it were that time.
                       Otherwise check in using the current time.
        """
        if not timestamp:
            timestamp = time.time()
        DAY = 60*60*24
        time_delta = min(DAY, timestamp - self.last_checkin)
        new_weight = 0.5*time_delta/DAY
        new_stress = self.get_current_stress(self.last_checkin + time_delta)
        self.stress = (1 - new_weight)*self.stress + new_weight*new_stress
        starve_time = self.last_fed + self.species.hunger_time
        new_time_fed = min(time_delta, starve_time - self.last_checkin)
        self.time_fed += new_time_fed
        self.last_checkin = timestamp

    def get_hunger(self, timestamp: float = None) -> float:
        """Gets how hungry the fish is.

        Based on the time since it was last fed and how quickly its species
        gets hungry.

        Args:
            timestamp: If provided, it will calculate how hungry the fish was
                       at that time. Otherwise it will use the current time.

        Returns:
            Float from 0-1 of how hungry the fish is with 0 being completely full
        """
        if not timestamp:
            timestamp = time.time()
        hunger = (timestamp - self.last_fed)/self.species.hunger_time
        return hunger

    def to_json(self) -> dict:
        """Gets dict for serializing to json

        Returns:
            Dict with all relevant information to serialize to json
        """
        json_object = {
            "name": self.name,
            "species": self.species.name,
            "personality": self.personality.name,
            "birth": self.birth,
            "last_fed": self.last_fed,
            "time_fed": self.time_fed,
            "stress": self.stress,
            "last_checkin": self.last_checkin,
        }
        return json_object
