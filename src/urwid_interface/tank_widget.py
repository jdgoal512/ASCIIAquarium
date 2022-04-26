import random
import threading
from typing import List

import urwid

from src.fish.fish import Fish
from src.urwid_interface.fish_art import FishArt
from src.urwid_interface.text_buffer import TextBuffer


BACKGROUND = [
    r'+==============================+',
    [r'|', ('water', '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'), '|'],
    r'|                              |',
    r'|                              |',
    r'|                              |',
    [r'|   ', ('green', 'o\o'), '                        |'],
    [r'|   ', ('green', 'o/o'), '                        |'],
    [r'|   ', ('green', 'o\o              \\\\  /'), '     |'],
    [r'|   ', ('green', 'o/o  o\\o        \\ \\| \\'), '     |'],
    [r'|   ', ('green', 'o\o  o/o         |/|//'), '     |'],
    [r'|   ', ('green', 'o/o  o\o          \|/'), '      |'],
    [r'+', ('sand', '##############################'), '+'],
]


class TankWidget(urwid.BoxAdapter):
    """Widget that has the shows the tank with the fish inside.

    Attributes:
        running: Whether or not the widget is running the animation.
        tank_width: Width of the interior of the tank in characters.
        tank_height: Height of the interior of the tank in characters.
        fish: FishArt for the fish in the tank.
        fish_lock: Mutex for safe handling of fish
        refresh_rate: How often to refresh the tank (in seconds)
    """
    def __init__(self, height: int,
                 width: int,
                 fish: List[FishArt] = None,
                 refresh_rate: float = 0.2,
                 background=BACKGROUND):
        self.running = False
        self.tank_width = width
        self.tank_height = height
        self.refresh_rate = refresh_rate
        self.text_buffer = TextBuffer(background)
        if fish:
            self.fish = fish
        else:
            self.fish = []
        self.fish_lock = threading.Lock()
        tank_rows = self.text_buffer.to_urwid()
        self.pile = urwid.Pile([urwid.Text(row) for row in tank_rows])
        super(TankWidget, self).__init__(urwid.Filler(self.pile),
                                         height=(self.tank_height + 3))

    def move_fish(self):
        """Randomly move the fish."""
        with self.fish_lock:
            for fish in self.fish:
                random_movement = random.random()
                if random_movement < 0.2*self.refresh_rate:
                    # Flip the fish
                    fish.flip()
                elif random_movement < 0.3*self.refresh_rate:
                    # Move up
                    if fish.y > 1:
                        fish.update_position(fish.x, fish.y - 1)
                    else:
                        # Bounce off top of tank
                        fish.update_position(fish.x, fish.y + 1)
                elif random_movement < 0.4*self.refresh_rate:
                    # Move down
                    if fish.y < self.tank_height:
                        fish.update_position(fish.x, fish.y + 1)
                    else:
                        # Bounce off bottom of tank
                        fish.update_position(fish.x, fish.y - 1)
                elif random_movement < 0.8*self.refresh_rate:
                    # Move forward
                    if fish.flipped:
                        if fish.x < self.tank_width - len(fish.get_art()):
                            # Move right
                            fish.update_position(fish.x + 1, fish.y)
                        else:
                            # Bounce off side of tank
                            fish.flip()
                    else:
                        if fish.x > 1:
                            # Move left
                            fish.update_position(fish.x - 1, fish.y)
                        else:  # Bounce off side of tank
                            fish.flip()

    def draw(self):
        """Move the fish and redraw the tank."""
        self.move_fish()
        self.text_buffer.clear()
        for fish in self.fish:
            self.text_buffer.add_text(x=fish.x,
                                    y=fish.y,
                                    text=fish.get_art(),
                                    formatting='goldfish')
        tank_rows = self.text_buffer.to_urwid()
        for pile_row, tank_row in zip(self.pile.contents, tank_rows):
            pile_row[0].set_text(tank_row)
            pile_row[0]._invalidate()

    def add_fish(self, fish: Fish):
        """Adds a fish to the tank as long as there is still room in the tank.

        Args:
            fish: The fish to be added.
        """
        x = random.randint(1, self.tank_width - len(fish.get_art()))
        y = random.randint(1, self.tank_height)
        with self.fish_lock:
            self.fish += [FishArt(fish, x, y)]

    def remove_fish(self, fish_name: str):
        """Remove the art for the fish with given name"""
        for fish in self.fish:
            if fish.fish.name == fish_name:
                with self.fish_lock:
                    self.fish.remove(fish)
                return

    def start_animation(self, loop: urwid.MainLoop):
        """Start the fish swimming.

        Args:
            loop: The main loop for urwid to call for schedule redraws.
        """
        if not self.running:
            self.running = True

            def redraw(*args):
                del args  # Unused
                if self.running:
                    self.draw()
                    loop.set_alarm_in(self.refresh_rate, redraw)
            redraw()

    def stop_animation(self):
        """Stop animating the fish."""
        self.running = False
