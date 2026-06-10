""" An improved version of the one written during the lightning talk. Adding e.g. command palette support for opening files.
Mainly an example used to show how it can be further extended with header, footer and opening files through the command palette.
"""

from argparse import ArgumentParser
from functools import partial
from pathlib import Path
from typing import cast
from textual.app import App
from textual.widgets import TextArea, DirectoryTree, Header, Footer
from textual.containers import Horizontal
from textual.command import Provider, Hit
from textual.binding import Binding

class Commands(Provider):
    def read_files(self, query="!(.*)"):
        res = []
        folders = [self.app.folder]
        while folders:
            folder = folders.pop()
            for p in folder.iterdir():
                if p.name.startswith("."):
                    continue
                if p.is_dir():
                    folders.append(p)
                else:
                    res.append(p)
        return res

    async def search(self, query):
        matcher = self.matcher(query)
        for path in self.read_files():
            command = f"open {path}"
            score = matcher.match(command)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(command),
                    partial(self.app.edit_file, path),
                    help="Open file in editor",
                )


class Editor(App):
    TITLE = "My Editor"

    CSS = """
    DirectoryTree {
        dock: left;
        width: 25%;
    }
    """

    COMMANDS = {Commands}

    BINDINGS = [
        Binding("ctrl+s", "save_file", "save current file"),
        Binding("ctrl+q", "quit", description="quit"),
        Binding("ctrl+p", "command_palette", description="open command palette")
    ]

    def __init__(self, folder, file=None):
        super().__init__()
        self.folder = folder
        self.file = file

    def compose(self):
        yield Header(show_clock=True)
        yield Horizontal(
            DirectoryTree(self.folder),
            TextArea("", read_only=True, id="editor"),
        )
        yield Footer()

    def on_ready(self):
        if self.file is not None:
            self.edit_file(self.file)

    def _on_directory_tree_file_selected(self, event):
        self.edit_file(event.path)

    def edit_file(self, path):
        if not path.is_file():
            return
        
        self.file = path
        text_editor = cast(TextArea, self.query_one("#editor"))
        text_editor.text = self.file.read_text()
        text_editor.language = "python" if self.file.suffix == ".py" else None
        text_editor.read_only = False
        text_editor.focus()

    def action_save_file(self):
        if self.file is None:
            return
        editor = self.query_one("#editor")
        self.file.write_text(editor.text)

if __name__ == "__main__":
#     parser = ArgumentParser("My Editor")
#     parser.add_argument("folder", type=Path)
    
#     args = parser.parse_args()
#     folder: Path = args.folder
    file = None

#     assert folder.exists()

#     if not folder.is_dir():
#         file = folder
#         folder = folder.parent

    app = Editor(".", file)
    app.run()