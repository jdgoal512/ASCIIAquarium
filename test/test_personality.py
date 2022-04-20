from pytest import fixture

from src.fish.personality import get_personalities


def test_get_personalities():
    all_personalities = get_personalities('test/personalities.json')
    assert len(all_personalities) == 1
    assert "DEV_PERSONALITY" in all_personalities.keys()
    dev_personality = all_personalities["DEV_PERSONALITY"]
    assert dev_personality.name == "DEV_PERSONALITY"


@fixture
def personality():
    return get_personalities('test/personalities.json')["DEV_PERSONALITY"]

def test_get_quote(personality):
    assert personality.get_quote('', 0, 0) == 'happy'
    assert personality.get_quote('', 0.25, 0) == 'normal'
    assert personality.get_quote('', 1, 0) == 'unhappy'
    hungry_quotes = [personality.get_quote('', 0, 1) for x in range(100)]
    assert 'hungry' in hungry_quotes

def test_to_json(personality):
    assert personality.to_json() == "DEV_PERSONALITY"
