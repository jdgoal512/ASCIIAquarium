import random

from src.fish.fish import Fish


def _double_replace(text: str, char1: str, char2: str) -> str:
    """Swaps instances of char1 and char2 in a string.

    Args:
        text: The text to do the replacements in.
        char1: One of the strings to swap.
        char2: The other of the strings to swap.

    Returns:
        A string with the substrings swapped
    """
    TEMP = '!@#$%^&temp!@#$%&'  # Giberish that would never actually show up
    text = text.replace(char1, TEMP)
    text = text.replace(char2, char1)
    text = text.replace(TEMP, char2)
    return text


def _reverse(text: str) -> str:
    """Reverses a line of ascii art.

    Flips directional characters like / and { as well.

    Args:
        text: String containing the ascii art to be flipped.

    Returns:
        String with the text reversed and directional characters replaced
        with their counterparts.
    """
    text = text[::-1]
    text = _double_replace(text, '<', '>')
    text = _double_replace(text, '{', '}')
    text = _double_replace(text, '(', ')')
    text = _double_replace(text, '[', ']')
    text = _double_replace(text, '/', '\\')
    return text


class FishArt:
    """Fish art and position.

    Attributes:
        fish: The fish the art is for.
        x: x position of the fish (0 is far left).
        y: y position of the fish (0 is top).
    """

    def __init__(self, fish: Fish, x: int, y: int):
        self.fish = fish
        self.x = x
        self.y = y
        self.flipped = random.random() > 0.5

    def flip(self):
        """Flip the art."""
        self.flipped = not self.flipped

    def update_position(self, x: int, y: int):
        """Change the position."""
        self.x = x
        self.y = y

    def get_art(self):
        """Get the art for the fish in the correct orientation."""
        fish_art = self.fish.get_art()
        # Randomly flip fish
        if self.flipped:
            fish_art = _reverse(fish_art)
        return fish_art
