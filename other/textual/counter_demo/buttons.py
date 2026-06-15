from textual import on
from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Middle, Center, ScrollableContainer, Center, Right
from textual.reactive import Reactive
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Button, Digits, Button, Static, TextArea, Label


class ConfirmExit(ModalScreen):
    """Popup z pytaniem o zamknięcie"""
    
    def compose(self):
        yield Vertical(
            Static("Czy chcesz zamknąć program?"),
            Horizontal(
                Button("Nie", id="no",  variant="primary"),
                Button("Tak", id="yes", variant="primary"),
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.app.exit()
        else:
            self.dismiss()   # zamyka popup


class Application(App):
    BINDINGS = [
        Binding("escape", "quit", "Wyjście", key_display="ESC"), # Wbudowane, nie trzeba definiować quit
        Binding("ctrl+q", "test", "Wyjście", show=False), # Wbudowane, nie trzeba definiować quit
        ("p", "pop_up", "Testowy pop-up"),
        ("t", "test", "Test"),
    ]
    
    CSS_PATH = "buttons.tcss"
    
    def compose(self):
        yield Header(name="Demo kontenerów", show_clock=True, icon=None)

        yield Vertical(
            Button("Czerwony",  id="red",   variant="error"),
            Button("Żółty",     id="yellow",variant="warning"),
            Button("Zielony",   id="green", variant="success"),
            Button("Niebieski", id="blue",  variant="primary"),
            Button("Czarny",    id="black", variant="default"),
            classes = "backgound_hatch"
        )

        # yield Button("Czerwony",  id="red",   variant="error")
        # yield Button("Żółty",     id="yellow",variant="warning")
        # yield Button("Zielony",   id="green", variant="success")
        # yield Button("Niebieski", id="blue",  variant="primary")
        # yield Button("Czarny",    id="black", variant="default")

        yield Footer()
        
    def on_mount(self):
        self.title = "Demo przycisków"

        header = self.query_one(Header)
        header.icon = "Menu"

        footer = self.query_one(Footer)
        footer.show_command_palette = False

    def action_test(self):
        print("test")
        self.notify("Test")
        
    def action_pop_up(self):
        self.push_screen(ConfirmExit())  # pokazanie popupu

    @on(Button.Pressed, "#red")
    def button_red(self):
        print("Wcisnąłeś czerwony przycisk")
        self.notify("Wcisnąłeś [b]czerwony[/b] przycisk", title="Błąd", severity="error")

    @on(Button.Pressed, "#yellow")
    def button_yellow(self):
        print("Wcisnąłeś żółty przycisk")
        self.notify("Wcisnąłeś [i]żółty[i] przycisk", title="Ostrzeżenie", severity="warning")
    
    @on(Button.Pressed, "#green")
    def button_green(self):
        print("Wcisnąłeś zielony przycisk")
        self.notify("Wcisnąłeś [u]zielony[/u] przycisk", title="Informacja", severity="information")

    @on(Button.Pressed, "#blue")
    def button_blue(self):
        print("Wcisnąłeś niebieski przycisk")
        self.notify("Wcisnąłeś niebieski przycisk", title="Informacja")

    @on(Button.Pressed, "#black")
    def button_black(self):
        print("Wcisnąłeś czarny przycisk")
        self.notify("Wcisnąłeś czarny przycisk")

if __name__ == "__main__":
    app = Application()
    app.run()
