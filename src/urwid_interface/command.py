from typing import Callable

class Command:
    """Holds data for each command line action.

    Attributes:
        name: The name of the command. If this text is inputted, this command
              will be called.
        action: Function to be called when this command is executed
        help_text: Text to display when the help function is called
        hidden: If True the help text will not be displayed from the help
                function

    """
    def __init__(self, name: str, action: Callable, help_text: str,
                 shortcuts=None, hidden: bool = False):
        self.name = name
        self.action = action
        self.help_text = help_text
        self.shortcuts = shortcuts
        self.hidden = hidden
