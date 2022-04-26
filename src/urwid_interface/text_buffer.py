from typing import List, Tuple, Union


class TextBuffer:
    """Text based buffer for drawing the the tank.

    Attributes:
        text: 2d array of characters for the background.
        formatting: 2d array of palette names for the background characters.
        foreground_text: 2d array of characters for the foreground.
        foreground_formatting: 2d array of palette names for the foreground.
    """

    def __init__(self, background):
        self.background = []
        self.formatting = []
        self.foreground_text = []
        self.foreground_formatting = []
        for row in background:
            text, formatting = self.read_row(row)
            self.background += [text]
            self.formatting += [formatting]
            self.foreground_text += [[None] * len(text)]
            self.foreground_formatting += [[None] * len(text)]

    def add_text(self, x: int, y: int, text: str, formatting: str = None):
        """Add text to the foreground.

        Args:
            x: X position for the text to start as.
            y: Y position for the text.
            text: Text to add to the foreground.
            formatting: Urwid palette name for the text.
        """
        for i, char in enumerate(text):
            self.foreground_text[y][x+i] = char
            self.foreground_formatting[y][x+i] = formatting

    def clear(self):
        """Clear the foreground."""
        self.foreground_text = []
        self.foreground_formatting = []
        for row in self.background:
            self.foreground_text += [[None] * len(row)]
            self.foreground_formatting += [[None] * len(row)]

    def get(self, x: int, y) -> str:
        """Get the character at (x, y).

        Args:
            x: x position of the character.
            y: y position of the character.
        """
        if self.foreground_text[y][x] is not None:
            return self.foreground_text[y][x], \
                   self.foreground_formatting[y][x]
        return self.background[y][x], self.formatting[y][x]

    def read_row(self, row) -> Tuple[List[str], List[str]]:
        """Read in a row of text.

        The row can be given as a string, or as a list of strings/tuples.
        Tuples are given in the format: (palette, text), with the palette
        being the string name of the urwid palette for formatting the text.
        """
        if isinstance(row, str):
            text = [character for character in row]
            formatting = [None] * len(row)
        else:
            text = []
            formatting = []
            for part in row:
                if isinstance(part, str):
                    text += [character for character in part]
                    formatting += [None] * len(part)
                else:
                    text += [character for character in part[1]]
                    formatting += [part[0]] * len(part[1])
        return text, formatting

    def to_urwid(self) -> List[Union[str, Tuple[str, str]]]:
        """Create list of formatted text for an urwid Text widget.

        Returns:
            List of strings or formatted strings suitable for setting as
            formatted text for an urwid Text widget.
        """
        all_rows = []
        for y in range(len(self.background)):
            row_text = []
            row_formatting = []
            current_text = ''
            current_formatting = None
            for x in range(len(self.background[y])):
                char, form = self.get(x, y)
                if form != current_formatting:
                    if current_text:
                        row_formatting += [current_formatting]
                        row_text += [current_text]
                        current_text = ''
                current_formatting = form
                current_text += char
            row_text += [current_text]
            row_formatting += [current_formatting]
            row = []
            for text_part, f_part in zip(row_text, row_formatting):
                if f_part is not None:
                    row += [(f_part, text_part)]
                else:
                    row += [text_part]
            if len(row) == 1:
                row = row[0]
            all_rows += [row]
        return all_rows


def main():
    text = [
        r'+==============================+',
        r'|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|',
        r'|                              |',
        r'|                              |',
        r'|                              |',
        r'|   o\o                        |',
        r'|   o/o                        |',
        r'|   o\o              \  /      |',
        r'|   o/o  o\o        \ \| \     |',
        r'|   o\o  o/o         |/|//     |',
        r'|   o/o  o\o          \|/      |',
        r'+##############################+',
    ]

    grid = TextBuffer(text)
    grid.add_text(x=15, y=1, text='fish', formatting='blue')
    rows = grid.to_urwid()
    grid.clear()
    breakpoint()

if __name__ == '__main__':
    main()
