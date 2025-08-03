import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder

# ── Window styling ─────────────────────────────────────────────────
Builder.load_file("gui/windows.kv")


# ── Window config ─────────────────────────────────────────────────

class VaultWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.entry_list = self.ids.entry_list
        self.search_input = self.ids.search_input
        self.selected = None

        self.populate_list()

    def populate_list(self):
        self.entry_list.clear_widgets()
        for label in ["GitHub", "Email", "Netflix", "Banking"]:
            btn = Button(
                text=label,
                size_hint_y=None,
                height=40,
                background_normal='',
                background_color=(0.25, 0.45, 0.75, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_release=self.on_select)
            self.entry_list.add_widget(btn)

    def on_select(self, button):
        self.selected = button.text
        print(f"Selected: {self.selected}")

    def handle_action(self, button):
        print(f"{button.text} button pressed")

        self.search_input = TextInput(
            hint_text="Search Labels",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.search_input)
        
        # Scrolling list area
        scroll_view = ScrollView()
        self.entry_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.entry_list.bind(minimum_height=self.entry_list.setter('height'))
        scroll_view.add_widget(self.entry_list)
        self.add_widget(scroll_view)
        

        button_row = BoxLayout(size_hint_y=None, height=50, spacing=10)
        for label in ["Add", "View", "Delete"]:
            action_btn = Button(text=label)
            action_btn.bind(on_release=self.handle_action)
            button_row.add_widget(action_btn)
            
        self.add_widget(button_row)

class HelloApp(App):
    def build(self):
        return VaultWindow()
    
if __name__=="__main__":
    HelloApp().run()

