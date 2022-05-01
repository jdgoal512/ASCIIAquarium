import random
from typing import List, Callable

import urwid

from src.tank import Tank
from src.urwid_interface.text_prompt import TextPrompt
from src.urwid_interface.tank_widget import TankWidget
from src.urwid_interface.popup import Popup


class Interface:
    """Command line interface for interacting with the tank and fish.

    Attributes:
        tank: The tank.
        bottom_widget: Urwid widget at the bottom of the tank.
        tank_widget: Urwid widget for ascii fish tank.
        palette: Urwid color palette.
        screen: Urwid screen for registering new palette entries.

    """
    def __init__(self, tank: Tank,
                 filename: str = 'save.json'):
        self.tank = tank
        self.filename = filename
        self.bottom_widget = None
        self.screen = None
        self.tank_widget = TankWidget(height=self.tank.height,
                                      width=self.tank.width)

        self.palette = [
            ('banner', '', '', '', '#ffa', '#60d'),
            ('green', '', '', '', '#151', ''),
            ('light_green', '', '', '', '#5c5', ''),
            ('sand', '', '', '', '#a81', ''),
            ('goldfish', '', '', '', '#ff1', ''),
            ('water', '', '', '', '#08b', ''),
            ('rock', '', '', '', '#587', ''),
        ]

        for fish in self.tank.fish:
            self.tank_widget.add_fish(fish)
            self.palette += [(f'fish_{fish.name}', '', '', '', fish.color, '')]

        self.loop = None

        menu_items = [
            ('Status', self.status_button_action),
            ('Feed', self.feed_button_action),
            ('Clean Tank', self.clean_button_action),
            ('Add a fish', self.add_fish_button_action),
            ('Remove a fish', self.remove_fish_button_action),
            ('Help', self.help_button_action),
            ('Quit', self.quit),
        ]
        body = []
        for label, action in menu_items:
            button = urwid.Button(label)
            urwid.connect_signal(button, 'click', action)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        self.main_menu_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def quit(self, _):
        """Exit the command line interface."""
        self.tank.save(self.filename)
        self.tank_widget.stop_animation()
        raise urwid.ExitMainLoop()

    def run(self):
        """Enter the urwid line interface."""
        self.bottom_widget = urwid.BoxAdapter(self.main_menu_widget, height=10)
        main_widget = urwid.Filler(urwid.Pile([urwid.Text('ASCII Aquarium'),
                                               self.tank_widget,
                                               urwid.Divider(),
                                               self.bottom_widget]))
        self.screen = urwid.raw_display.Screen()
        self.loop = urwid.MainLoop(main_widget, self.palette, screen=self.screen)
        self.loop.screen.set_terminal_properties(colors=256)
        self.tank_widget.start_animation(self.loop)
        self.loop.run()

    def menu(self, title: str, choices: List[str], callback: Callable,
             cancel_button: bool = True):
        """Create a menu.

        Creates a menu with the given title and list of choices and an optional
        "Cancel" button which goes back to the main menu. Selecting another
        item passes the name of that item to the callback function.

        Args:
            title: Title for the menu.
            choices: List of choices the user can pick from.
            callback: Function to call with the string the user picked.
            cancel_button: Whether or not to add a cancel button.
        """
        body = [urwid.Text(title), urwid.Divider()]
        for choice in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', callback, choice)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        if cancel_button:
            button = urwid.Button('Cancel')
            urwid.connect_signal(button, 'click', self.main_menu)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        list_box = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.bottom_widget.original_widget = list_box

    def status_button_action(self, _):
        """Get the status of all fish."""
        status = '\n'.join(self.tank.get_status())
        popup = Popup(message=('yellow', status), callback=self.main_menu)
        self.bottom_widget.original_widget = popup

    def feed_button_action(self, _):
        """Feed the fish."""
        self.tank.feed()
        popup = Popup(message='The fish have been feed', callback=self.main_menu)
        self.bottom_widget.original_widget = popup

    def clean_button_action(self, _):
        """Feed the fish."""
        response = self.tank.clean()
        popup = Popup(message=response, callback=self.main_menu)
        self.bottom_widget.original_widget = popup

    def main_menu(self, *args):
        """Go back to the main menu."""
        del args  # Unused
        self.bottom_widget.original_widget = self.main_menu_widget

    def add_fish_button_action(self, _):
        """Add a fish to the tank.

        The user is given a list of species and then asked to name it. Duplicate
        names are not allowed. A random personality is selected and a fish is
        created using these parameters and added to the tank.
        """
        if self.tank.is_full():
            popup = Popup('Sorry, the tank is full', self.main_menu)
            self.bottom_widget.original_widget = popup
        else:
            self.menu('Choose a species for your fish:',
                      list(self.tank.fish_builder.species.keys()),
                      self.get_fish_name)

    def get_fish_name(self, _, species: str):
        """Gets a name for the fish.

        Opens a text prompt for the user to name their fish. Also picks a
        random personality for the fish and then passes it to a callback to
        add the fish to the tank.

        Args:
            species: Name of the species to make the fish.
        """
        personalities = list(self.tank.fish_builder.personalities.keys())
        personality = random.choice(personalities)

        def add_fish(name):
            """Add the fish to the tank and go back to the main menu.

            Adds the fish if there is not already another one with the
            same name (not case sensitive).

            Args:
                name: The name of the fish.
            """
            # Check if the name is already taken
            if name.lower() in [fish.name.lower() for fish in self.tank.fish]:
                current_widget = self.bottom_widget.original_widget

                def back_to_name(*args):
                    """Go back to the fish naming screen"""
                    del args  # Unused
                    self.bottom_widget.original_widget = current_widget
                popup = Popup('Sorry, that name is already taken', back_to_name)
                self.bottom_widget.original_widget = popup
                return

            new_fish = self.tank.fish_builder.make_fish(name=name,
                                                        species_name=species,
                                                        personality_name=personality)
            self.tank.add_fish(new_fish)
            self.screen.register_palette_entry(name=f'fish_{new_fish.name}',
                                             foreground='',
                                             background='',
                                             mono='',
                                             foreground_high=new_fish.color,
                                             background_high='')
            self.tank_widget.add_fish(new_fish)
            self.main_menu()
        name_prompt = TextPrompt(f'What do you want to name your {species}?\n', add_fish)
        self.bottom_widget.original_widget = name_prompt

    def remove_fish_button_action(self, _):
        """Remove a fish from the tank.

        The user is given a list of fish to choose one to remove or to cancel.
        After selecting one, the user is prompted to make sure they want to. If
        so the fish is removed.
        """
        if self.tank.fish:
            fish_names = [fish.name for fish in self.tank.fish]
            self.menu('Select a fish to remove:', fish_names,
                      self.verify_remove_fish)
        else:
            popup = Popup('There are no fish to remove', self.main_menu)
            self.bottom_widget.original_widget = popup

    def verify_remove_fish(self, _, fish_name):
        """Double checks if you really want to remove a fish then removes it.

        Args:
            fish_name: The name of the fish to remove
        """
        def remove_fish(_, response):
            """Remove the fish.

            Removes the fish if the user said so, then goes back to the main menu.

            Args:
                response: "Yes" or "No" whether or not to remove the fish.
            """
            if response == 'Yes':
                message = self.tank.remove_fish(fish_name)
                self.tank_widget.remove_fish(fish_name)
                popup = Popup(message=message, callback=self.main_menu)
                self.bottom_widget.original_widget = popup
            else:
                self.main_menu()
        self.menu('Are you sure?', ['Yes', 'No'], remove_fish, cancel_button=False)

    def help_button_action(self, _):
        """Prints the help message."""
        help_message = 'Feed your fish every day to make them happy.'
        help_message += ' It will take a while for them to grow up.'
        popup = Popup(help_message, self.main_menu)
        self.bottom_widget.original_widget = popup
