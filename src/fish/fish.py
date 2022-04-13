import time

from src.fish.species import Species
from src.fish.personality import Personality


class Fish:
    def __init__(self,
                 name: str,
                 species: Species,
                 personality: Personality,
                 last_fed: float = None,
                 birth: float = None,
                 stress: float = 0.25,
                 last_checkin: float = None):
        self.name = name
        self.species = species
        self.personality = personality
        self.stress = stress
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

    def get_status(self):
        self.checkin()
        quote = self.personality.get_quote(name=self.name, stress=self.stress, hunger=self.get_hunger())
        return f'{self.name} ({self.species.name}): {quote}'

    def feed(self):
        hunger = (time.time() - self.last_fed)/self.species.hunger_time
        if hunger > 0.2:
            self.last_fed = time.time()
        else:
            print(f'{self.name} is not hungry yet')

    def get_stress_text(self) -> str:
        if self.stress < 0.05:
            return 'Very happy'
        if self.stress < 0.1:
            return 'Happy'
        if self.stress < 0.2:
            return 'Feels ok'
        if self.stress < 0.3:
            return 'A little stressed'
        if self.stress < 0.5:
            return 'Stressed'
        return 'Dangerously stressed'

    def get_current_stress(self, timestamp: float = None):
        if not timestamp:
            timestamp = time.time()

        hunger = self.get_hunger(timestamp)
        hunger = max(0, (hunger - 0.5)/0.5)
        # TODO: add other stressors
        stress = hunger
        return stress

    def checkin(self, timestamp: float = None):
        """
        Reavaluate stress, etc

        Should not be used without a timestamp if over 24 hours has
        passed since the last checkin
        """
        if not timestamp:
            timestamp = time.time()
        DAY = 60*60*24
        time_delta = min(DAY, timestamp - self.last_checkin)
        new_weight = 0.5 * time_delta / DAY
        new_stress = self.get_current_stress(self.last_checkin + time_delta)
        self.stress = ((1 - new_weight) * self.stress) + (new_weight * new_stress)
        self.last_checkin = timestamp

    def get_hunger(self, timestamp: float = None) -> float:
        if not timestamp:
            timestamp = time.time()
        hunger = (timestamp - self.last_fed)/self.species.hunger_time
        return hunger

    def get_hunger_text(self, timestamp: float = None) -> str:
        hunger = self.get_hunger(timestamp)
        if hunger > 1:
            return 'Starved to death'
        if hunger >= 0.5:
            return 'Starving'
        if hunger > 0.4:
            return 'Very Hungry'
        if hunger > 0.3:
            return 'Hungry'
        if hunger > 0.2:
            return 'A little hungry'
        return 'Full'

    def to_json(self):
        json_object = {
            "name": self.name,
            "species": self.species.name,
            "personality": self.personality.name,
            "birth": self.birth,
            "last_fed": self.last_fed,
            "stress": self.stress,
            "last_checkin": self.last_checkin,
        }
        return json_object


def main():
    fish = Fish('Molly', 'Mosquitofish')
    print(fish.get_status())
    fish.feed()
    print(fish.get_status())
    j_fish = fish.to_json()
    print(j_fish)
    print(fish.to_json())
    fish_copy = Fish.from_json(j_fish)

    breakpoint()

if __name__ == '__main__':
    main()
