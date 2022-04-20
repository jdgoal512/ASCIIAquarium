import random
import threading
from typing import List

import urwid

from src.fish.fish import Fish
from src.urwid_interface.fish_art import FishArt


class TankWidget(urwid.BoxAdapter):
    """Widget that has the shows the tank with the fish inside.

    Attributes:
        running: Whether or not the widget is running the animation.
        tank_width: Width of the interior of the tank in characters.
        tank_height: Height of the interior of the tank in characters.
        fish: FishArt for the fish in the tank.
        fish_lock: Mutex for safe handling of fish
    """
    def __init__(self, height: int, width: int, fish: List[FishArt] = None):
        self.running = False
        self.tank_width = width
        self.tank_height = height
        if fish:
            self.fish = fish
        else:
            self.fish = []
        self.fish_lock = threading.Lock()
        tank_rows = self.get_tank_rows()
        self.pile = urwid.Pile([urwid.Text(row) for row in tank_rows])
        super(TankWidget, self).__init__(urwid.Filler(self.pile),
                                         height=(self.tank_height + 3))

    def move_fish(self, refresh_rate: float = 1):
        """Randomly move the fish.

        Args:
            refresh_rate: How many times this is called per second.
        """
        with self.fish_lock:
            for fish in self.fish:
                random_movement = random.random()
                if random_movement < 0.2*refresh_rate:  # Flip the fish
                    fish.flip()
                elif random_movement < 0.3*refresh_rate:  # Move up
                    if fish.y > 1:
                        fish.update_position(fish.x, fish.y - 1)
                    else:  # Bounce off top of tank
                        fish.update_position(fish.x, fish.y + 1)
                elif random_movement < 0.4*refresh_rate:  # Move down
                    if fish.y <= self.height:
                        fish.update_position(fish.x, fish.y + 1)
                    else:  # Bounce off bottom of tank
                        fish.update_position(fish.x, fish.y - 1)
                elif random_movement < 0.8*refresh_rate:  # Move forward
                    if fish.flipped:
                        if fish.x <= self.tank_width - len(fish.get_art()):  # Move right
                            fish.update_position(fish.x + 1, fish.y)
                        else:  # Bounce off side of tank
                            fish.flip()
                    else:
                        if fish.x > 1:  # Move left
                            fish.update_position(fish.x - 1, fish.y)
                        else:  # Bounce off side of tank
                            fish.flip()

    def get_tank_rows(self, interval: float = 1) -> List[str]:
        """Create ascii art of the tank with all the fish inside.

        Args:
            interval: How many times this is called per second.

        Returns:
            A list of strings with the ascii art for the tank.
        """
        tank_text = ["+" + '=' * self.tank_width + '+']
        tank_text += ["|" + '~' * self.tank_width + '|']
        for _ in range(self.tank_height):
            tank_text += ["|" + ' ' * self.tank_width + '|']
        tank_text += ["+" + '#' * self.tank_width + '+']
        self.move_fish(interval)
        with self.fish_lock:
            for fish in self.fish:
                fish_art = fish.get_art()
                tank_text[fish.y] = tank_text[fish.y][:fish.x] + fish_art \
                    + tank_text[fish.y][fish.x + len(fish_art):]
        return tank_text

    def draw(self, interval=1):
        """Redraw the tank."""
        tank_rows = self.get_tank_rows(interval)
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

    def start_animation(self, loop: urwid.MainLoop, interval: float = 1):
        """Start the fish swimming.

        Args:
            loop: The main loop for urwid to call for schedule redraws.
        """
        if not self.running:
            self.running = True

            def redraw(*args):
                del args  # Unused
                if self.running:
                    self.draw(interval)
                    loop.set_alarm_in(interval, redraw)
            redraw()

    def stop_animation(self):
        """Stop animating the fish."""
        self.running = False
