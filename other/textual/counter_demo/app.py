from textual.app import App
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Button, Static

class TimeDisplay(Static):
    pass

class Stopwatch(Static):
    def compose(self):
        yield Button("Czerwony", variant="error")
        yield Button("Żółty", variant="warning")
        yield Button("Zielony", variant="success")
        yield Button("Niebieski", variant="primary")
        yield Button("Czarny", variant="default")
        yield Button("Reset")
        yield TimeDisplay("00:00:00.00")
    
class StopwatchApp(App):
    BINDINGS = [
        ("d,ctrl+a", "toggle_dark_mode", "Toggle light/dark mode")
    ]
    
    def compose(self):
        self.theme = "textual-dark"
        yield Header(show_clock=True)
        with ScrollableContainer(id="stopwatches"):
            yield Stopwatch()
            yield Stopwatch()
            yield Stopwatch()
#         yield ScrollableContainer(
#             Stopwatch(),
#             Stopwatch(),
#             Stopwatch(),
#             id="stopwatches"
#         )
        yield Footer()
        
    def action_toggle_dark_mode(self):
        if self.theme == "textual-light":
            self.theme = "textual-dark"
        else:
            self.theme = "textual-light"

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()