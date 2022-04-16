from typing import List
import random

import urwid

from src.cmd_interface.color import Color
from src.cmd_interface.command import Command
from src.tank import Tank


class Interface:
    """Command line interface for interacting with the tank and fish.

    Attributes:
        tank: The tank
        color: Whether or not to enable printing in color
        commands: List of commands the interface has
    """
    def __init__(self, tank: Tank, filename: str = 'save.json', color: bool = True):
        self.tank = tank
        self.filename = filename
        self.color = color
        self.bottom_panel = None
        self.commands = [
            Command(name='help',
                    action=self.help,
                    help_text='Show this message',
                    shortcuts=['h', 'help']),
            Command(name='feed',
                    action=self.feed,
                    help_text='Show this message',
                    shortcuts=['f', 'feed']),
            Command(name='status',
                    action=self.status,
                    help_text='Get the status of the fish',
                    shortcuts=['s', 'status']),
            Command(name='add_fish',
                    action=self.add_fish,
                    help_text='Add a fish to the tank',
                    shortcuts=['a', 'add_fish']),
            Command(name='remove_fish',
                    action=self.remove_fish,
                    help_text='Remove a fish from the tank',
                    shortcuts=['r', 'remove_fish']),
            Command(name='debug',
                    action=self.debug,
                    help_text='Enter pdb',
                    hidden=True),
            Command(name='quit',
                    action=self.quit,
                    help_text='Quit',
                    shortcuts=['q', 'quit', 'e', 'exit']),
        ]


    def _print(self, text, color=None, end='\n'):
        """Prints the given text in the given color.

        Args:
            text: Text to print.
            color: Color for the text. If None, then it is not colored.
            end: End of the line. Set to "" to continue printing on the same
                 line.
        """
        if self.color and color:
            print(f'{color.value}{text}{Color.RESET.value}', end=end)
        else:
            print(text, end=end)

    def help(self, _):
        """Prints the help message."""
        self._print('Commands:', Color.YELLOW)
        for command in self.commands:
            if not command.hidden:
                if command.shortcuts:
                    for shortcut in command.shortcuts:
                        self._print(shortcut, Color.CYAN, end='')
                        if shortcut != command.shortcuts[-1]:
                            self._print('/', end='')
                else:
                    self._print(command.name, Color.CYAN, end='')
                self._print(f': {command.help_text}')

    def quit(self, _):
        """Exit the command line interface."""
        # self._print('Exiting')
        self.tank.save(self.filename)
        raise urwid.ExitMainLoop()

    def _process_cmd(self, cmd: str):
        """Process a line of text.

        The first word is the command. The rest of the words are passed as a
        list to the the command function. If an invalid command is entered it
        displays an error message.
        """
        for command in self.commands:
            if command.shortcuts:
                if cmd in command.shortcuts:
                    command.action()
                    return
            elif cmd == command.name:
                command.action()
                return
        self._print('Invalid command, type "help" for help', Color.RED)

    def run(self):
        """Enter the urwid line interface."""
        main_widget = urwid.Filler(urwid.Pile([urwid.Text('ASCII Aquarium'),
                                   urwid.Divider(),
                                   urwid.BoxAdapter(self.main_menu(), height=10)]))
        loop = urwid.MainLoop(main_widget)
        # loop = urwid.MainLoop(self.main_menu())
        loop.run()

    def main_menu(self):
        body = []
        for command in self.commands:
            button = urwid.Button(command.name)
            urwid.connect_signal(button, 'click', command.action)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def menu(self, title: str, choices: List[str]):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.feed, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        list_box = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        return urwid.Overlay(list_box,
                             bottom_w,
                             align,
                             width,
                             valign,
                             height)

    # def menu(self, prompt: str, choices: List[str]) -> str:
    #     """Creates a menu.

    #     The user is given a numbered list of options. Entering the number
    #     or name of the item (not case sensitive) selects that item. If the
    #     user gives an invalid input, they are prompted again until they give
    #     valid input. The user can also quit the program by entering "q" or
    #     "quit".

    #     Args:
    #         prompt: String with a prompt/title for the menu.
    #         choices: List of items the user can choose from.

    #     Returns:
    #         String with the choice the user selected. If the user chose to
    #         quit instead, None is returned instead.

    #     """
    #     choice = None
    #     while True:
    #         self._print(prompt, Color.YELLOW)
    #         for i, choice_name in enumerate(choices):
    #             self._print(i+1, Color.CYAN, end='')
    #             self._print(f'. {choice_name}')
    #         choice = input('> ')
    #         try:
    #             index = int(choice)
    #             if 0 < index <= len(choices):
    #                 choice = choices[index - 1]
    #         except ValueError:
    #             pass
    #         lower_choices = [x.lower() for x in choices]
    #         lower_choice = choice.lower()
    #         if lower_choice in lower_choices:
    #             choice = choices[lower_choices.index(lower_choice)]
    #             break
    #         if lower_choice in ('q', 'quit'):
    #             self.quit()
    #             return None
    #         self._print('Invalid selection', Color.RED)
    #     return choice

    def feed(self, _):
        """Feed the fish."""
        self.tank.feed()

    def status(self, _):
        """Print the tank and get the status of the tank and fish."""
        self.tank.print()

    def debug(self, _):
        """Enter pdb."""
        breakpoint()

    def add_fish(self, _):
        """Add a fish to the tank

        The user is given a list of species and then asked to name it. Duplicate
        names are not allowed. A random personality is selected and a fish is
        created using these parameters and added to the tank.
        """
        if self.tank.is_full():
            self._print('Sorry, the tank is full', Color.RED)
            return
        species = self.menu('Choose a species for your fish:',
                            list(self.tank.fish_builder.species.keys()))
        if species is None:  # User quit instead of picking species
            return
        personalities = list(self.tank.fish_builder.personalities.keys())
        personality = random.choice(personalities)
        name_taken = True
        while name_taken:
            name_taken = False
            name = input('What do you want to name your fish? ')
            for fish in self.tank.fish:
                if fish.name.lower() == name.lower():
                    self._print('Sorry, that name is already taken', Color.RED)
                    name_taken = True
                    break
        new_fish = self.tank.fish_builder.make_fish(name=name,
                                                    species_name=species,
                                                    personality_name=personality)
        self.tank.add_fish(new_fish)
        self.tank.print()

    def remove_fish(self, _):
        """Remove a fish from the tank

        The user is given a list of fish to choose one to remove or to cancel.
        After selecting one, the user is prompted to make sure they want to. If
        so the fish is removed.
        """
        fish_names = [fish.name for fish in self.tank.fish]
        fish_name = self.menu('Select a fish to remove:', [*fish_names, 'Cancel'])
        if not fish_name:  # User quit
            return
        if fish_name == 'Cancel' and 'Cancel' not in fish_names:  # Cancel
            self.tank.print()
            return
        verification = self.menu('Are you sure?', ['Yes', 'No'])
        if not verification:  # User quit
            return
        if verification == 'Yes':
            self.tank.remove_fish(fish_name)
        self.tank.print()
