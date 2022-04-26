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
    max_x = DEFAULT_WIDTH - len(sample_fish.species.art[0])
    fish += [FishArt(sample_fish, x=max_x, y=DEFAULT_HEIGHT)]
    fish += [FishArt(sample_fish, x=max_x, y=DEFAULT_HEIGHT)]
    fish += [FishArt(sample_fish, x=max_x, y=DEFAULT_HEIGHT)]
    return TankWidget(height=DEFAULT_HEIGHT,
                      width=DEFAULT_WIDTH,
                      fish=fish,
                      refresh_rate=1)


def test_move_fish(tank_widget):
    for _ in range(1000):
        tank_widget.move_fish()
        for fish in tank_widget.fish:
            assert 0 < fish.x <= DEFAULT_WIDTH - len(fish.get_art())
            assert 0 < fish.y <= DEFAULT_HEIGHT
