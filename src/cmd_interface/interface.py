from typing import List

from src.cmd_interface.color import Color
from src.cmd_interface.command import Command
from src.tank import Tank


class Interface:
    """Command line interface for interacting with the tank and fish.

    Attributes:
        tank: The tank
        running: Whether or not the interface is running
        color: Whether or not to enable printing in color
        commands: List of commands the interface has
    """
    def __init__(self, tank: Tank, filename: str = 'save.json', color: bool = True):
        self.tank = tank
        self.running = False
        self.filename = filename
        self.color = color
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

    def help(self, *args: List[str]):
        """Prints the help message."""
        del args # Not needed
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

    def quit(self, *args: List[str]):
        """Exit the command line interface."""
        del args # Not needed
        self._print('Exiting')
        self.running = False
        self.tank.save(self.filename)

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
        """Enter the command line interface."""
        self.running = True
        self.tank.print()
        self.help()
        while self.running:
            cmd = input('> ')
            print('')
            cmd = cmd.lower().strip()
            self._process_cmd(cmd)

    # def _menu(self, prompt, choices):
    #     choice = None
    #     while True:
    #         self._print(prompt, Color.YELLOW)
    #     for i, choice_name in enumerate(choices):
    #     self._print(i+1, Color.CYAN, end='')
    #     self._print(f'. {choice_name}')
    #     choice = input('> ')
    #     try:
    #     index = int(choice)
    #     if 0 < index <= len(choices):
    #     choice = choices[index - 1]
    #     except ValueError:
    #     pass
    #     if choice in choices:
    #     break
    #     if choice in ('q', 'quit'):
    #     self.quit()
    #     return None
    #     self._print('Invalid selection', Color.RED)
    #     return choice

    def feed(self, *args: List[str]):
        """Feed the fish."""
        del args # Not needed
        self.tank.feed()

    def status(self, *args: List[str]):
        """Print the tank and get the status of the tank and fish."""
        del args # Not needed
        self.tank.print()

    def debug(self, *args: List[str]):
        """Enter pdb."""
        del args # Not needed
        breakpoint()
