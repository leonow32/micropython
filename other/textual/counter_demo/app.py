from textual.app import App
from textual.widgets import Header, Footer, Button

class StopwatchApp(App):
    BINDINGS = [
        ("d,ctrl+a", "toggle_dark_mode", "Toggle light/dark mode")
    ]
    
    def compose(self):
        self.theme = "textual-light"
        yield Header(show_clock=True)
        yield Button("Start")
        yield Button("Stop")
        yield Footer()
        
    def action_toggle_dark_mode(self):
        if self.theme == "textual-dark":
            self.theme = "textual-light"
        else:
            self.theme = "textual-dark"

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()