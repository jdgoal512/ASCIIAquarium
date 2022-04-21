from pytest import fixture, raises
import time

from src.fish.fish import Fish
from src.fish.fish_builder import FishBuilder
from src.tank import Tank, DEFAULT_HEIGHT, DEFAULT_WIDTH, DEFAULT_MAX_FISH

DAY = 60*60*24
FISH_NAME = 'DEFAULT_FISH'

@fixture
def fish():
    builder = FishBuilder(species_file='test/species.json',
                          personality_file='test/personalities.json')
    return builder.make_fish(FISH_NAME,
                             species_name='DEV_FISH',
                             personality_name='DEV_PERSONALITY')


@fixture
def tank():
    return Tank(last_checkin=1)


def test_add_fish(tank, fish):
    assert len(tank.fish) == 0
    tank.add_fish(fish)
    assert len(tank.fish) == 1
    for _ in range(DEFAULT_MAX_FISH):
        tank.add_fish(fish)
    assert len(tank.fish) == DEFAULT_MAX_FISH


def test_is_full(tank, fish):
    assert len(tank.fish) == 0
    assert not tank.is_full()
    tank.add_fish(fish)
    assert not tank.is_full()
    for _ in range(DEFAULT_MAX_FISH):
        tank.add_fish(fish)
    assert tank.is_full()


def test_remove_fish(tank, fish):
    assert len(tank.fish) == 0
    assert tank.remove_fish(FISH_NAME) == f'Error, could not remove {FISH_NAME}'
    tank.add_fish(fish)
    assert len(tank.fish) == 1
    assert tank.remove_fish(FISH_NAME) != f'Error, could not remove {FISH_NAME}'
    assert len(tank.fish) == 0
    for _ in range(DEFAULT_MAX_FISH):
        tank.add_fish(fish)
    assert len(tank.fish) == DEFAULT_MAX_FISH
    for _ in range(DEFAULT_MAX_FISH):
        assert tank.remove_fish(FISH_NAME) != f'Error, could not remove {FISH_NAME}'
    assert len(tank.fish) == 0


def test_feed(tank, fish):
    fish.last_fed = 0
    tank.last_checkin = time.time()
    tank.add_fish(fish)
    assert tank.fish[0].last_fed == 0
    tank.feed()
    assert tank.fish[0].last_fed != 0


def test_clean(tank, fish):
    current_time = time.time()
    tank.last_checkin = current_time
    assert tank.waste == 0
    tank.checkin(current_time + DAY)
    assert tank.waste == 0
    tank.add_fish(fish)
    tank.checkin(current_time + DAY*2)
    assert tank.waste != 0
    tank.last_checkin = current_time  # Reset checkin time
    tank.clean()
    assert tank.waste != 0
    tank.checkin(current_time + DAY*200)
    assert tank.waste != 0
    tank.last_checkin = current_time  # Reset checkin time
    tank.clean()
    assert tank.waste < 0.01
