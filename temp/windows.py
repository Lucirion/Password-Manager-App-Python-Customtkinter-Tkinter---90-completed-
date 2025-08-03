from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button    import Button
from kivy.uix.dropdown  import DropDown

# gui/windows.py

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

# Load KV definitions
Builder.load_file('windows.kv')

class ThemeColors:
    """Hold your theme properties on the App instance."""
    primary_color = [0.2, 0.6, 0.86, 1]
    bg_color      = [0.15, 0.15, 0.15, 1]
    text_color    = [1, 1, 1, 1]
    input_bg      = [0.25, 0.25, 0.25, 1]
    border_color  = [0.5, 0.5, 0.5, 1]

class VaultWindow(BoxLayout):
    vault = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vault = vault

class MenuBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal",
                         size_hint_y=None, height=40,
                         spacing=5, padding=5, **kwargs)

        # 1) Create the dropdown and bind its on_select
        self.dropdown = DropDown()
        self.dropdown.bind(on_select=self.on_select)

        # 2) Populate it with buttons
        for option in ("Import", "Export", "Settings"):
            btn = Button(text=option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        # 3) Main menu button opens the dropdown
        self.mainbutton = Button(text="Menu",
                                 size_hint_x=None, width=100,
                                 height=40)
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.add_widget(self.mainbutton)

    def on_select(self, dropdown, selection):
        # This is called *once* when you call dropdown.select(...)
        self.mainbutton.text = f"{selection}"
        dropdown.dismiss()
        print("You picked:", selection)
