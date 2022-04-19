import urwid

from src.tank import Tank


class TankWidget(urwid.BoxAdapter):
    """Widget that has the shows the tank with the fish inside

    Attributes:
        tank: The tank to show
    """
    def __init__(self, tank: Tank):
        self.tank = tank
        self.tank_rows = tank.draw_tank()
        self.running = False
        self.pile = urwid.Pile([urwid.Text(row) for row in self.tank_rows])
        super(TankWidget, self).__init__(urwid.Filler(self.pile), height=(tank.height + 3))

    def draw(self, interval=1):
        """Redraw the tank."""
        self.tank_rows = self.tank.draw_tank(interval)
        for pile_row, tank_row in zip(self.pile.contents, self.tank_rows):
            pile_row[0].set_text(tank_row)
            pile_row[0]._invalidate()

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
