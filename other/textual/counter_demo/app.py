from time import monotonic

from textual import on
from textual.app import App
from textual.containers import ScrollableContainer
from textual.reactive import Reactive
from textual.widgets import Header, Footer, Button, Static

class TimeDisplay(Static):
    time_elapsed = Reactive(0)
    start_time = monotonic()
    
    def on_mount(self):
        # To się wywołuje kiedy TimeDisplay jest tworzony
        self.update_timer = self.set_interval(1/60, self.update_time_elapsed, pause=True)
    
    def update_time_elapsed(self):
        self.time_elapsed = monotonic() - self.start_time
    
    def watch_time_elapsed(self):
        time = self.time_elapsed
        time, seconds = divmod(time, 60)
        hours, minutes = divmod(time, 60)
        time_str = f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"
        self.update(time_str)
        
    def start(self):
        print("TimeDisplay.start")
        self.start_time = monotonic()
        self.update_timer.resume()
    
    def stop(self):
        print("TimeDisplay.stop")
        self.time_elapsed = monotonic() - self.start_time
        self.update_timer.pause()
    
    def reset(self):
        print("TimeDisplay.reset")
        self.start_time = monotonic()
#         self.update("123456")
        

class Stopwatch(Static):
    
    @on(Button.Pressed, "#start")
    def start_stopwatch(self):
        print("Wciśnięto start")
        self.add_class("running")
        self.remove_class("idle")
        self.query_one(TimeDisplay).start()
#         self.app.exit()

    @on(Button.Pressed, "#stop")
    def stop_stopwatch(self):
        print("Wciśnięto stop")
        self.add_class("idle")
        self.remove_class("running")
        
#         time_display = self.query_one("TimeDisplay")
#         time_display.time_elapsed = 12*3600+34*60+56
        self.query_one(TimeDisplay).stop()
        
    @on(Button.Pressed, "#reset")
    def reset_button(self):
        print("Wciśnięto reset")
        self.query_one(TimeDisplay).reset()
        
    def compose(self):
#         yield Button("Czerwony", variant="error")
#         yield Button("Żółty", variant="warning")
#         yield Button("Zielony", variant="success")
#         yield Button("Niebieski", variant="primary")
        yield Button("Start", variant="success", id="start")
        yield Button("Stop",  variant="error",   id="stop")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")
    
class StopwatchApp(App):
    BINDINGS = [
        ("d,ctrl+a", "toggle_dark_mode", "Toggle light/dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]
    
    CSS_PATH = "stopwatch.tcss"
    
    def compose(self):
        self.theme = "textual-dark"
        yield Header(name="Zegar", show_clock=True)
        with ScrollableContainer(id="stopwatches"):
            yield Stopwatch(classes="idle")
            yield Stopwatch(classes="idle")
            yield Stopwatch(classes="idle")
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
    
    def action_add_stopwatch(self):
        stopwatch = Stopwatch()
        stopwatch.add_class("idle")
        container = self.query_one("#stopwatches")
        container.mount(stopwatch)
        stopwatch.scroll_visible() # przeskroluj ekran, aby nowo utworzony zegar był widoczny
        
    def action_remove_stopwatch(self):
        stopwatches = self.query(Stopwatch)
        print(f"len(stopwatches) = {len(stopwatches)}, type(stopwatches) = {type(stopwatches)}")
        
        if stopwatches:
            stopwatches.last().remove()

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()