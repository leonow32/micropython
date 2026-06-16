from textual import on
from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, HorizontalGroup, HorizontalScroll, Vertical, VerticalScroll, Middle, Center, ScrollableContainer, Center, Right
from textual.reactive import Reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Collapsible, Digits, Footer, Header, Label, Markdown, Static, Tabs, TabbedContent, TabPane, TextArea

from my_widgets.confirm_exit import ConfirmExit

EXAMPLE_MARKDOWN = """\
## Markdown

- Typography *emphasis*, **strong**, `inline code` etc.    
- Headers    
- Lists    
- Syntax highlighted code blocks
- Tables and more

## Quotes

> I must not fear.
> > Fear is the mind-killer.
> > Fear is the little-death that brings total obliteration.
> > I will face my fear.
> > > I will permit it to pass over me and through me.
> > > And when it has gone past, I will turn the inner eye to see its path.
> > > Where the fear has gone there will be nothing. Only I will remain.

## Tables

| Name            | Type   | Default | Description                        |
| --------------- | ------ | ------- | ---------------------------------- |
| `show_header`   | `bool` | `True`  | Show the table header              |
| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |
| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |

## Code blocks

```python
def loop_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    \"\"\"Iterate and generate a tuple with a flag for last value.\"\"\"
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value
```


"""

class Application(App):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        Binding("escape", "confirm_exit", "Wyjście", key_display="ESC"), # Wbudowane, nie trzeba definiować quit
        Binding("ctrl+q", "test", "Wyjście", show=False), # Wbudowane, nie trzeba definiować quit
        ("p", "pop_up", "Testowy pop-up"),
        ("t", "test", "Test"),
    ]
    
    def compose(self):
        yield Header(name="Demo kontenerów", show_clock=True, icon=None)
        # yield Static("")
        # yield Label("x")

        with TabbedContent(): # initial="buttons"

            with TabPane("Markdown", id="markdown"):
                with VerticalScroll():
                    yield Markdown(EXAMPLE_MARKDOWN)

            with TabPane("Digits", id="digits"):
                with Center():
                    digits1 = Digits("0123456789")
                    digits1.border_title = "Title"
                    yield digits1
                    digits2 = Digits("ABCDEF")
                    digits2.border_subtitle = "Subtitle"
                    yield digits2

            with TabPane("Static", id="static_scroll"):
                yield ScrollableContainer(
                    Label(f"Lorem ipsum dolor sit amet 1", classes="box"),
                    Label(f"Lorem ipsum dolor sit amet 2", classes="box"),
                    Label(f"Lorem ipsum dolor sit amet 3", classes="box"),
                    Label(f"Lorem ipsum dolor sit amet 4", classes="box"),
                    Label(f"Lorem ipsum dolor sit amet 5", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 6", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 7", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 8", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 9", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 10", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 11", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 12", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 13", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 14", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 15", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 16", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 17", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 18", classes="box"),
                    # Static(f"Lorem ipsum dolor sit amet 19", classes="box"),
                    # Label("label", classes="box"), 
                )

            with TabPane("Przyciski", id="buttons"):
                yield Button("Czerwony",  id="red",   variant="error")
                yield Button("Żółty",     id="yellow",variant="warning")
                yield Button("Zielony",   id="green", variant="success")
                yield Button("Niebieski", id="blue",  variant="primary")
                yield Button("Czarny",    id="black", variant="default")
            
            
            
            with TabPane("Lorem Ipsum", id="lorem"):
                yield ScrollableContainer(
                # with VerticalScroll():
                    Label(f"Lorem ipsum dolor sit amet 1", classes="box"),
                    Label("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                    Label("label") ,
                    classes="box"
                )
                
            with TabPane("Ustawienia", id="settings"):
                with ScrollableContainer():
                    with Collapsible(title="Ogólne", collapsed=True):
                        with Horizontal():
                            yield Button("Czerwony",  id="red",   variant="error")
                            yield Button("Żółty",     id="yellow",variant="warning")
                            yield Button("Zielony",   id="green", variant="success")
                            yield Button("Niebieski", id="blue",  variant="primary")
                            yield Button("Czarny",    id="black", variant="default")
                            # yield Button("Czerwony",  id="red2",   variant="error")
                            # yield Button("Żółty",     id="yellow2",variant="warning")
                            # yield Button("Zielony",   id="green2", variant="success")
                            # yield Button("Niebieski", id="blue2",  variant="primary")
                            # yield Button("Czarny",    id="black2", variant="default")
                    with Collapsible(title="Aaaaaaaaaaaa", collapsed=True):
                        with HorizontalGroup():
                            yield Button("Czerwony",  id="red",   variant="error")
                            yield Button("Żółty",     id="yellow",variant="warning")
                            yield Button("Zielony",   id="green", variant="success")
                            yield Button("Niebieski", id="blue",  variant="primary")
                            yield Button("Czarny",    id="black", variant="default")
                            yield Button("Czerwony",  id="red2",   variant="error")
                            yield Button("Żółty",     id="yellow2",variant="warning")
                            yield Button("Zielony",   id="green2", variant="success")
                            yield Button("Niebieski", id="blue2",  variant="primary")
                            yield Button("Czarny",    id="black2", variant="default")
                    with Collapsible(title="Kolejna karta", collapsed=True):
                        with HorizontalScroll():
                            yield Button("Czerwony",  id="red",   variant="error")
                            yield Button("Żółty",     id="yellow",variant="warning")
                            yield Button("Zielony",   id="green", variant="success")
                            yield Button("Niebieski", id="blue",  variant="primary")
                            yield Button("Czarny",    id="black", variant="default")
                            yield Button("Czerwony",  id="red2",   variant="error")
                            yield Button("Żółty",     id="yellow2",variant="warning")
                            yield Button("Zielony",   id="green2", variant="success")
                            yield Button("Niebieski", id="blue2",  variant="primary")
                            yield Button("Czarny",    id="black2", variant="default")

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

    def action_confirm_exit(self):
        self.push_screen(ConfirmExit())

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
        self.notify("Wcisnąłeś [blue]niebieski[/blue] przycisk", title="Informacja")

    @on(Button.Pressed, "#black")
    def button_black(self):
        print("Wcisnąłeś czarny przycisk")
        self.notify("Wcisnąłeś czarny przycisk")

if __name__ == "__main__":
    app = Application()
    app.run()
