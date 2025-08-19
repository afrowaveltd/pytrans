# ui/palette.py
from __future__ import annotations
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Input, ListView, ListItem, Label
from textual.events import Key

BUILTIN_THEMES = [
    "textual-dark", "textual-light", "nord", "gruvbox",
    "catppuccin-mocha", "dracula", "tokyo-night", "monokai",
    "flexoki", "catppuccin-latte", "solarized-light",
]

class PaletteScreen(ModalScreen[str | None]):
    """Lokalizovaná paleta: režim příkazů a motivů."""
    CSS = """
    PaletteScreen {
        align: center middle;
    }
    #card {
        width: 80%;
        height: 60%;
        border: round $accent;
        background: $panel;
    }
    #search {
        dock: top;
        height: 3;
        padding: 0 1;
    }
    #list {
        height: 1fr;
        overflow: auto;
    }
    """

    def __init__(self, mode: str = "commands") -> None:
        super().__init__()
        self.mode = mode  # "commands" | "themes"

    def compose(self) -> ComposeResult:
        i18n = getattr(self.app, "i18n", None)
        t = (i18n.t if i18n else (lambda k, **v: k))

        yield Label("", id="card")  # jen kvůli boxu (stylování)
        yield Input(placeholder=t("pal.placeholder.commands"), id="search")
        yield ListView(id="list")

    def on_mount(self) -> None:
        self._refresh_items()

    def _refresh_items(self, query: str = "") -> None:
        i18n = getattr(self.app, "i18n", None)
        t = (i18n.t if i18n else (lambda k, **v: k))
        lv = self.query_one("#list", ListView)
        lv.clear()

        def add(key: str, desc_key: str, value: str) -> None:
            name = t(key)
            desc = t(desc_key)
            if query and query.casefold() not in (name + " " + desc).casefold():
                return
            li = ListItem(Label(name), Label(desc))
            li.data = value # type: ignore
            lv.append(li)

        if self.mode == "commands":
            # naše „aliasy“ na akce aplikace
            add("cmd.change_theme", "cmd.change_theme.desc", "cmd:theme")
            add("cmd.maximize", "cmd.maximize.desc", "cmd:maximize")
            add("cmd.quit", "cmd.quit.desc", "cmd:quit")
            add("cmd.save_screenshot", "cmd.save_screenshot.desc", "cmd:screenshot")
            add("cmd.show_help", "cmd.show_help.desc", "cmd:help")
        else:
            # motivy: Textual built-in + náš AS400
            themes = BUILTIN_THEMES + ["as400"]
            for th in themes:
                # přeložený popisek motivu, když existuje
                key = f"theme.{th}" if i18n and i18n.has(f"theme.{th}") else th
                add(key, "theme.description", f"theme:{th}")

    def on_input_changed(self, event: Input.Changed) -> None:
        self._refresh_items(event.value)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        data = event.item.data # type: ignore
        if not data:
            return
        if data == "cmd:theme":
            # přepnout do režimu výběru motivů
            self.mode = "themes"
            ph = self.app.i18n.t("pal.placeholder.themes") if hasattr(self.app, "i18n") else "Search for themes..." # type: ignore
            self.query_one("#search", Input).placeholder = ph
            self.query_one("#search", Input).value = ""
            self._refresh_items("")
            return

        if data == "cmd:maximize":
            self.app.maximize() # type: ignore
        elif data == "cmd:quit":
            self.app.exit()
        elif data == "cmd:screenshot":
            self.app.save_screenshot()
        elif data == "cmd:help":
            self.app.action_show_help_panel()
        elif data.startswith("theme:"):
            theme = data.split(":", 1)[1]
            if hasattr(self.app, "apply_theme"):
                self.app.apply_theme(theme) # type: ignore

        self.dismiss(None)

    def on_key(self, event: Key) -> None:
        if event.key == "escape":
            self.dismiss(None)
