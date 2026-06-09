""" Simple code editor using textual. Live coded during the lightning talk in about 7 minutes
"""

from argparse import ArgumentParser
from pathlib import Path
from textual.app import App
from textual.widgets import TextArea, DirectoryTree
from textual.containers import Horizontal

class Editor(App):

    BINDINGS = [
        ("ctrl+s", "save_file"),
        ("ctrl+q", "quit"),
    ]

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.file = None

    def compose(self):
        yield Horizontal(
            DirectoryTree(self.folder),
            TextArea("", id="editor")
        )

    def _on_directory_tree_file_selected(self, event):
        path: Path = event.path
        if not path.is_file():
            return
        
        self.file = path
        
        text_editor = self.query_one("#editor")
        text_editor.text = self.file.read_text()
        text_editor.language = "python" if self.file.suffix == ".py" else None

    def action_save_file(self):
        if self.file is None:
            return
        editor = self.query_one("#editor")
        self.file.write_text(editor.text)

if __name__ == "__main__":
#     parser = ArgumentParser("My Editor")
#     parser.add_argument("folder", type=Path)
#     
#     args = parser.parse_args()
#     folder: Path = args.folder
# 
#     if not folder.exists():
#         raise FileNotFoundError(f"No folder found for path: {folder}")
# 
#     if not folder.is_dir():
#         folder = folder.parent
    
#     app = Editor(folder)
    app = Editor(".")
    app.run()