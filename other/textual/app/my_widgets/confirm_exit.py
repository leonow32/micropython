from textual import on
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static

class ConfirmExit(ModalScreen):
    """Popup z pytaniem o zamknięcie"""

    CSS_PATH = "confirm_exit.tcss"

    BINDINGS = [
        Binding("escape", "close", "Zamknij"),
    ]
    
    def compose(self):


        yield Vertical(
            Static("Czy chcesz zamknąć program?"),
            Horizontal(
                Button("Tak", id="yes", variant="warning"),
                Button("Nie", id="no",  variant="warning"),
            )
        )

    def action_close(self):
        self.dismiss()

    @on(Button.Pressed, "#no")
    def button_no(self):
        self.dismiss()   # zamyka popup

    @on(Button.Pressed, "#yes")
    def button_yes(self):
        self.app.exit() 
