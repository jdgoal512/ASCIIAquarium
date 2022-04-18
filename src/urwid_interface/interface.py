from typing import List
import random

import urwid

from src.cmd_interface.color import Color
from src.cmd_interface.command import Command
from src.tank import Tank


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(u'Nice to meet you,\n%s.\n\nPress Q to exit.' % edit.edit_text)

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
        self.bottom_widget = None

        self.commands = [
            Command(name='Feed',
                    action=self.feed,
                    help_text='Show this message',
                    shortcuts=['f', 'feed']),
            Command(name='Add a fish',
                    action=self.add_fish,
                    help_text='Add a fish to the tank',
                    shortcuts=['a', 'add_fish']),
            Command(name='Remove a fish',
                    action=self.remove_fish,
                    help_text='Remove a fish from the tank',
                    shortcuts=['r', 'remove_fish']),
            # Command(name='Help',
            #         action=self.help,
            #         help_text='Show this message',
            #         shortcuts=['h', 'help']),
            Command(name='Quit',
                    action=self.quit,
                    help_text='Quit',
                    shortcuts=['q', 'quit', 'e', 'exit']),
        ]
        body = []
        for command in self.commands:
            button = urwid.Button(command.name)
            urwid.connect_signal(button, 'click', command.action)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        self.main_menu_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))


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
        self.bottom_widget = urwid.BoxAdapter(self.main_menu_widget, height=10)
        main_widget = urwid.Filler(urwid.Pile([urwid.Text('ASCII Aquarium'),
                                        urwid.Divider(),
                                        self.bottom_widget]))
        loop = urwid.MainLoop(main_widget)
        loop.run()

    def main_menu(self):
        body = []
        for command in self.commands:
            button = urwid.Button(command.name)
            urwid.connect_signal(button, 'click', command.action)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def menu(self, title: str, choices: List[str], callback, cancel_button=True):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', callback, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        if cancel_button:
            button = urwid.Button('Cancel')
            urwid.connect_signal(button, 'click', self.main_menu)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        list_box = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.bottom_widget.original_widget = list_box

    def feed(self, _):
        """Feed the fish."""
        self.tank.feed()

    def main_menu(self, *args):
        del args  # Unused
        self.bottom_widget.original_widget = self.main_menu_widget

    def add_fish(self, _):
        """Add a fish to the tank

        The user is given a list of species and then asked to name it. Duplicate
        names are not allowed. A random personality is selected and a fish is
        created using these parameters and added to the tank.
        """
        if self.tank.is_full():
            self._print('Sorry, the tank is full', Color.RED)
            return
        self.menu('Choose a species for your fish:',
                  list(self.tank.fish_builder.species.keys()),
                  self.name_fish)

    def name_fish(self, _, species):
        personalities = list(self.tank.fish_builder.personalities.keys())
        personality = random.choice(personalities)

        # edit = urwid.Pile([urwid.Edit(f'What do you want to name your {species}?\n', edit_text='hello', wrap='clip')])
        # edit = urwid.BoxAdapter(urwid.Pile([urwid.Edit(f'What do you want to name your {species}?\n', edit_text='hello', wrap='clip')]), height=10)
        #edit = urwid.BoxAdapter(urwid.Edit(f'What do you want to name your {species}?\n', edit_text='hello', wrap='clip'), height=10)
        edit = urwid.Edit(f'What do you want to name your {species}?\n')
        fill = QuestionBox(edit)

        # self.bottom_widget.original_widget = EditText(f'What do you want to name your {species}?\n',
        #                                               self.main_menu, self.main_menu)
        self.bottom_widget.original_widget = fill
        # self.bottom_widget.original_widget = urwid.Edit(f'What do you want to name your {species}?\n')
        # import time; time.sleep(20)
        # while name_taken:
        #     name_taken = False
        #     name = input('What do you want to name your fish? ')
        #     for fish in self.tank.fish:
        #         if fish.name.lower() == name.lower():
        #             self._print('Sorry, that name is already taken', Color.RED)
        #             name_taken = True
        #             break
        # new_fish = self.tank.fish_builder.make_fish(name=name,
        #                                             species_name=species,
        #                                             personality_name=personality)
        # self.main_menu()

    def remove_fish(self, _):
        """Remove a fish from the tank

        The user is given a list of fish to choose one to remove or to cancel.
        After selecting one, the user is prompted to make sure they want to. If
        so the fish is removed.
        """
        fish_names = [fish.name for fish in self.tank.fish]
        fish_name = self.menu('Select a fish to remove:', fish_names,
                              self.double_check_remove_fish)

    def double_check_remove_fish(self, _, fish_name):
        def callback(_, response):
            if response == 'Yes':
                self.tank.remove_fish(fish_name)
            self.main_menu()
        self.menu('Are you sure?', ['Yes', 'No'], callback, cancel_button=False)
