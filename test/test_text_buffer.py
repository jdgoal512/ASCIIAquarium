from pytest import fixture

from src.urwid_interface.text_buffer import TextBuffer
from src.urwid_interface.tank_widget import BACKGROUND
from src.tank import DEFAULT_HEIGHT, DEFAULT_WIDTH


@fixture
def text_buffer():
    text = [
        r'+==============================+',
        r'|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|',
        r'|                              |',
        r'|                              |',
        r'|                              |',
        [r'|   o\o    ', ('blue', 'fish'), '                |'],
        r'|   o/o                        |',
        r'|   o\o              \  /      |',
        r'|   o/o  o\o        \ \| \     |',
        r'|   o\o  o/o         |/|//     |',
        r'|   o/o  o\o          \|/      |',
        r'+##############################+',
    ]
    return TextBuffer(text)


def test_to_urwid(text_buffer):
    rows = text_buffer.to_urwid()
    for row in rows:
        if isinstance(row, str):
            assert len(row) == DEFAULT_WIDTH + 2
        else:
            actual_row = ''
            for part in row:
                if isinstance(part, str):
                    actual_row += part
                else:
                    actual_row += part[-1]
            assert len(actual_row) == DEFAULT_WIDTH + 2
