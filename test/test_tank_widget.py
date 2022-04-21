from pytest import fixture

from src.fish.fish_builder import FishBuilder
from src.urwid_interface.fish_art import FishArt
from src.urwid_interface.tank_widget import TankWidget
from src.tank import DEFAULT_HEIGHT, DEFAULT_WIDTH


@fixture
def tank_widget():
    builder = FishBuilder(species_file='test/species.json',
                          personality_file='test/personalities.json')
    sample_fish = builder.make_fish('Fishy',
                                    species_name='DEV_FISH',
                                    personality_name='DEV_PERSONALITY')
    fish = []
    fish += [FishArt(sample_fish, x=1, y=1)]
    fish += [FishArt(sample_fish, x=1, y=1)]
    fish += [FishArt(sample_fish, x=1, y=1)]
    fish += [FishArt(sample_fish, x=DEFAULT_WIDTH, y=DEFAULT_HEIGHT)]
    fish += [FishArt(sample_fish, x=DEFAULT_WIDTH, y=DEFAULT_HEIGHT)]
    fish += [FishArt(sample_fish, x=DEFAULT_WIDTH, y=DEFAULT_HEIGHT)]
    return TankWidget(height=DEFAULT_HEIGHT,
                      width=DEFAULT_WIDTH,
                      fish=fish,
                      refresh_rate=1)


def test_get_rows(tank_widget):
    """Check for any IndexErrors while moving fish"""
    for _ in range(1000):
        tank_widget.get_tank_rows()
