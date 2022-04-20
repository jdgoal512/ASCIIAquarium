from typing import Callable

import urwid


class Popup(urwid.Filler):
    """Display a popup message with an "OK" button.

    Attributes:
        message: Message to display in the popup
    """
    def __init__(self, message: str, callback: Callable):
        ok_button = urwid.Button('OK')
        urwid.connect_signal(ok_button, 'click', callback)
        pile = urwid.Pile([urwid.Text(message), ok_button])
        super(Popup, self).__init__(pile, valign='top')
