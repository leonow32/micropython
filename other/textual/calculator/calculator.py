from textual import on
from textual.app import App
from textual.containers import Horizontal, Vertical, ScrollableContainer, Center, Right
from textual.reactive import Reactive
from textual.widgets import Header, Footer, Digits, Button, Static, TextArea, Label

class CalculatorApp(App):
    BINDINGS = [
        ("d,ctrl+a", "toggle_dark_mode", "Toggle light/dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]
    
    CSS_PATH = "calculator.tcss"
    
    def compose(self):
        yield Header(name="Kalkulator", show_clock=True)

        yield Right(
            Digits("0123456789", classes="box"),
            Label("aaa", classes="box"),
            Digits("ABCdEFGHIJKLMNOPQRSTUVWXYZ.,:;'\"", classes="box"),
            classes="box"
        )

        # with Center():
        #     Digits("0123456789")
        #     Digits("ABCDEFGHIJ")

        yield Vertical(
            # Digits("3.141,592,653,5897"),
            # TextArea(),
            # TextArea(),
            Static("aaa", classes="box"),
            Static("bbb", classes="box"),
            classes="box"
        )
        yield Footer()
        
    def on_mount(self):
        self.title = "Kalkulator"

        footer = self.query_one(Footer)
        footer.show_command_palette = False
        
   

if __name__ == "__main__":
    app = CalculatorApp()
    app.run()