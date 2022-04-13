"""
Holds data for each command line action
"""
class Command:
    def __init__(self, name: str, action, help_text: str,
                 shortcuts=None, hidden: bool = False):
        self.name = name
        self.action = action
        self.help_text = help_text
        self.shortcuts = shortcuts
        self.hidden = hidden
