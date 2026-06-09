""" Simple code editor using textual. Live coded during the lightning talk in about 7 minutes
"""

# from pathlib import Path
from textual.app import App
from textual.widgets import Footer, Header, TextArea
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

class Main(App):
    TITLE = "Testowa aplikacja w Textual"

    BINDINGS = [
        Binding("ctrl+.", "testing"),
    ]

    def __init__(self):
        super().__init__()

#     def compose(self):
#         yield Vertical(
#             TextArea("aaaaaa", id="editor1"),
#             TextArea("bbbbbb", id="editor2"),
#             TextArea("cccccc", id="editor3"),
#         )
    
#     def compose(self):
#         yield Horizontal(
#             TextArea("aaaaaa", id="editor1"),
#             TextArea("bbbbbb", id="editor2"),
#             TextArea("cccccc", id="editor3"),
#         )

    def compose(self):
        yield Header(show_clock=True)
        yield Vertical(
            TextArea("editor1", id="editor1"),
            TextArea("editor2", id="editor2"),
            Horizontal(
                TextArea("editor3", id="editor3"),
                TextArea("editor4", id="editor4"),
                Vertical(
                    TextArea("editor5", id="editor5"),
                    TextArea("editor6", id="editor6"),
                    TextArea("editor7", id="editor7"),
                )
            )
        )
        yield Footer()

#     def _on_directory_tree_file_selected(self, event):
#         path: Path = event.path
#         if not path.is_file():
#             return
#         
#         self.file = path
#         
#         text_editor = self.query_one("#editor")
#         text_editor.text = self.file.read_text()
#         text_editor.language = "python" if self.file.suffix == ".py" else None
# 
#     def action_save_file(self):
#         if self.file is None:
#             return
#         editor = self.query_one("#editor")
#         self.file.write_text(editor.text)

    def action_testing(self):
        editor = self.query_one("#editor1")
        text_editor.text = "To jest testowa akcja przypisana do CTRL-1"

if __name__ == "__main__":
    app = Main()
    app.run()
