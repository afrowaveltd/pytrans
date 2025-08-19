
from __future__ import annotations
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, ContentSwitcher, Static
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.screen import ModalScreen

from services.settings_service import Settings
from services.localization_service import LocalizationService
from ui.views.hub import HubView
from ui.icons import icon
from ui.palette import PaletteScreen
from services.rtl_service import RTLService
from pathlib import Path

class ConfirmScreen(ModalScreen[bool]):
    def __init__(self, title="Neuložené změny", text="Opravdu přejít jinam? Změny se nemusí uložit."):
        super().__init__()
        self._title = title
        self._text = text

    def compose(self) -> ComposeResult:
        yield Static(f"🔒 {self._title}\n\n{self._text}\n", id="confirm-text")
        with Horizontal(id="confirm-buttons"):
            yield Button("✔️ Ano", id="ok")
            yield Button("✖️ Ne", id="cancel")

        CSS = """
    Screen { layout: vertical; }
    #topbar { dock: top; height: 3; padding: 0 1; background: $surface; }
    Footer { dock: bottom; }
    #body { height: 1fr; overflow: hidden auto; }
    #spacer { width: 1; }

    /* RTL režim – jednoduché zarovnání textu a pořadí prvků */
    .-rtl * { text-align: right; }
    .-rtl #topbar { direction: rtl; }

    /* AS400 vzhled (pokud nepoužiješ themes/as400.tcss) */
    .-as400 {
        background: #001a00;
        color: #8cff66;
    }
    .-as400 Header, .-as400 Footer, .-as400 #topbar {
        background: #002100;
        color: #8cff66;
        border: tall #00aa00;
    }
    .-as400 Button {
        background: #002600;
        color: #8cff66;
        border: round #00aa00;
    }
    .-as400 Button.-active, .-as400 Button:focus {
        background: #003000;
        color: #b8ff8f;
        border: round #00cc00;
    }
    """


    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "ok")

class DummyView(Static):
    def __init__(self, label: str, **kwargs):
        super().__init__(**kwargs)
        self._label = label
    def compose(self) -> ComposeResult:
        yield Static(self._label + "\n(Později sem přijde obsah)")

class PyTransApp(App):
    CSS = '\nScreen { layout: vertical; }\n#topbar { dock: top; height: 3; padding: 0 1; background: $surface; }\nFooter { dock: bottom; }\n#body { height: 1fr; overflow: hidden auto; }\n#spacer { width: 1; }\n'
    BINDINGS = [
        ("b", "go_back", "Zpět"),
        ("ctrl+h", "go_home", "Domů"),
        ("ctrl+p", "open_palette", "Příkazy"),
    ]

    route: reactive[str] = reactive("hub")
    _history: list[str] = []

    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.t = LocalizationService(self.settings.language)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="topbar"):
            # bezpečné 1-cell ikony přes icon_set
            icon_set = getattr(self, "icon_set", "text")
            yield Button(f"{icon('back', icon_set)} {self.t.t("app.back")}".strip(), id="nav-back")
            yield Button(f"{icon('home', icon_set)} {self.t.t("app.home")}".strip(), id="nav-home")
            yield Static("", id="spacer")
        with ContentSwitcher(id="body", initial="hub"):
            yield HubView(id="hub")
            yield DummyView("🎯 Cíle", id="targets")
            yield DummyView("⏱️ Plánovač", id="scheduler")
            yield DummyView("🧩 Pluginy", id="plugins")
            yield DummyView("📚 Slovníky", id="dictionaries")
            yield DummyView("⚙️ Nastavení", id="settings")
        yield Footer()

    def watch_route(self, value: str) -> None:
        self.query_one(ContentSwitcher).current = value

    async def _can_leave_current(self) -> bool:
        # extend later with dirty-checks
        return True

    async def go(self, target: str) -> None:
        if target == self.route:
            return
        if await self._can_leave_current():
            self._history.append(self.route)
            self.route = target

    async def back(self) -> None:
        if self._history and await self._can_leave_current():
            self.route = self._history.pop()

    async def home(self) -> None:
        if await self._can_leave_current():
            self._history.clear()
            self.route = "hub"

    async def action_go_back(self) -> None:
        await self.back()

    async def action_go_home(self) -> None:
        await self.home()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "nav-back":
            await self.back()
        elif event.button.id == "nav-home":
            await self.home()

    def on_mount(self) -> None:
        # icon set
        try:
            self.icon_set = self.settings.get("icon_set", "text")  # type: ignore[attr-defined]
        except Exception:
            self.icon_set = getattr(self.settings, "icon_set", "text") if hasattr(self, "settings") else "text"

        # RTL podpora
        rtl_path = Path("locales/languages.json")
        self._rtl = RTLService(rtl_path)
        current_lang = getattr(self.settings, "language", None) if hasattr(self, "settings") else "en"
        lang_str = current_lang if isinstance(current_lang, str) and current_lang is not None else "en"
        if self._rtl.is_rtl(lang_str):
            self.screen.add_class("-rtl")
        else:
            self.screen.remove_class("-rtl")

        # Motiv při startu
        theme = getattr(self.settings, "theme", None) if hasattr(self, "settings") else None
        if theme:
            self.apply_theme(theme)
        else:
            self.theme_name = "textual-dark"

    # --- Lokalizovaná paleta ---
    def action_open_palette(self) -> None:
        self.push_screen(PaletteScreen("commands"))

    # --- Motivy: built-in + AS400 ---
    def apply_theme(self, name: str) -> None:
        """Nastaví motiv; podporuje Textual built-in a 'as400'."""
        self.theme_name = name
        # nejprve očisti případné třídy
        self.screen.remove_class("-as400")
        if name == "as400":
            # Použij vlastní TCSS pokud existuje, jinak CSS třídu níže
            tfile = Path("themes/as400.tcss")
            if tfile.exists():
                # načti a aplikuj jako dodatečné styly
                self.stylesheet.read(str(tfile))
                self.refresh_css()
            self.screen.add_class("-as400")
        else:
            try:
                self.theme = name  # Textual built-in
            except Exception:
                # fallback
                self.theme = "textual-dark"
        # zapiš do settings (pokud služba existuje)
        try:
            self.settings["theme"] = name  # type: ignore[index]
            self.save_settings()  # vždy zavolej helper
        except Exception:
            pass

    def save_settings(self) -> None:
        """Uloží nastavení do persistentního úložiště, pokud je k dispozici."""
        if hasattr(self.settings, "save_settings"):
            self.settings.save_settings()


if __name__ == "__main__":
    PyTransApp().run()
