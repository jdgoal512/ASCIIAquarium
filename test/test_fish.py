from pytest import fixture
import time

from src.fish.fish import Fish
from src.fish.species import get_species
from src.fish.personality import get_personalities


DAY = 60*60*24


@fixture
def fish():
    species = get_species('test/species.json')
    personalities = get_personalities('test/personalities.json')
    return Fish(name='',
                species=species['DEV_FISH'],
                personality=personalities['DEV_PERSONALITY'],
                last_fed=0,
                birth=0,
                stress=0,
                last_checkin=0,
                time_fed=0)


def test_feeding(fish):
    assert fish.last_fed == 0
    fish.feed()
    assert fish.last_fed > 0
    last_fed = fish.last_fed
    fish.feed()
    assert fish.last_fed == last_fed


def test_get_hunger(fish):
    assert fish.last_fed == 0
    assert fish.get_hunger(0) == 0
    assert fish.species.hunger_time == 10
    assert fish.get_hunger(fish.species.hunger_time/2) == 0.5
    assert fish.get_hunger(fish.species.hunger_time) == 1.0
    fish.checkin(DAY)
    assert fish.get_hunger() == 1


def test_stress(fish):
    assert fish.stress == 0
    fish.checkin(DAY)
    assert 0 < fish.stress <= 1


def test_time_fed(fish):
    assert fish.species.hunger_time == 10
    hunger_time = fish.species.hunger_time
    assert fish.time_fed == 0
    fish.checkin(100)
    assert fish.time_fed == 10
    fish.last_fed = 100  # Feed it
    fish.checkin(200)
    assert fish.time_fed == 20
    fish.last_fed = 200  # Feed it
    fish.checkin(205)
    assert fish.time_fed == 25
