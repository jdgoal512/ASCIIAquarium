from typing import Callable

import urwid


class TextPrompt(urwid.Filler):
    """Creates a prompt with an edit text.

    Attributes:
        text: The text to display in the prompt.
        callback: Function to pass the entered text to when "enter" is pressed.
    """
    def __init__(self, text: str, callback: Callable):
        self.edit = urwid.Edit(text, edit_text='', wrap='clip')
        super(TextPrompt, self).__init__(self.edit, valign='top')
        self.callback = callback

    def keypress(self, size: int, key: str):
        if key != 'enter':
            return super(TextPrompt, self).keypress(size, key)
        self.callback(self.edit.edit_text)
