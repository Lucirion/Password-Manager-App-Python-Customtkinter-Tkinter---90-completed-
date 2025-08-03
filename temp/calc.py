from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

Window.size = (400, 600)

class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exit_check(self, *args):
        self.counter += 1
        if self.counter < 5:
            self.text = str(self.counter)
            return True  # block app's exit
        else:
            return False  # let the app close

    # Build out the app
        self.result = TextInput(
            font_seize=45,
            size_hint_y=0.2,
            readonly=True,
            halign="right",
            multiline=False,
        )
        self.add_widget(self.result)

        # Create buttons
        Buttons = [
            'C', '+/-', 
        ]

        grid = GridLayout(cols=4, spacing=5, padding=10)
        for row in buttons:
            for item in row:
                button = Button(
                    text=item,
                    font_size=32,
            )
            grid.add_widget(button)
        self.add_widget(grid)
class CalculatorApp(App):
    def build(self):
        return Calculator()


if __name__=="__main__":
    CalculatorApp().run()


