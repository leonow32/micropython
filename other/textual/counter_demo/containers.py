from textual import on
from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer, Center, Right
from textual.reactive import Reactive
from textual.widgets import Header, Footer, Digits, Button, Static, TextArea, Label

class Application(App):
    BINDINGS = [
        Binding("escape", "quit", "Wyjście", key_display="ESC"), # Wbudowane, nie trzeba definiować quit
        ("d,ctrl+a", "toggle_dark_mode", "Toggle light/dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]
    
    CSS_PATH = "containers.tcss"
    
    def compose(self):
        yield Header(name="Demo kontenerów", show_clock=True)

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
    app = Application()
    app.run()
