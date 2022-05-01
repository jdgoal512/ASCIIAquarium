from pytest import fixture

from src.fish.species import get_species


def test_get_species():
    all_species = get_species('test/species.json')
    assert len(all_species) == 1
    assert "DEV_FISH" in all_species.keys()
    dev_species = all_species["DEV_FISH"]
    assert dev_species.name == "DEV_FISH"


@fixture
def species():
    return get_species('test/species.json')["DEV_FISH"]


def test_get_species_art(species):
    assert species.get_art(0) == "baby"
    assert species.get_art(15) == "juvenile"
    assert species.get_art(101) == "adult"


def test_colors(species):
    assert species.get_color() in ["#f00", "#0f0", "#00f"]
    colors = [species.get_color() for _ in range(100)]
    assert "#f00" in colors
    assert "#0f0" in colors
    assert "#00f" in colors

def test_to_json(species):
    assert species.to_json() == "DEV_FISH"
