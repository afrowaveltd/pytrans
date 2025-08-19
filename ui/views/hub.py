
from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Static
from textual import events
from textual.widget import Widget
from ..icons import icon

class HubView(Widget):
    """Hub — big buttons with emoji, colors via CSS."""

    DEFAULT_CSS = '\nHubView {\n    padding: 1 2;\n}\nGrid#hub-grid {\n    grid-size: 3;\n    grid-gutter: 1 1;\n    grid-rows: auto;\n    width: 100%;\n    height: auto;\n}\n.tile {\n    height: 5;\n    content-align: center middle;\n    border: round $primary;\n    text-style: bold;\n}\n.success { border: round $success; background: $success 10%; }\n.warning { border: round $warning; background: $warning 8%; }\n.info    { border: round $accent;  background: $accent  8%; }\n.danger  { border: round $error;   background: $error  8%; }\n.neutral { border: round $secondary; background: $surface 3%; }\n#hub-title { padding: 0 1; }\n'

    def compose(self) -> ComposeResult:
        app = self.app  # type: ignore
        t = getattr(app, "t", None)
        if t is None or not hasattr(t, "t"):
            class DummyT:
                def t(self, s): return s
            t = DummyT()
        icon_set = getattr(self.app, "icon_set", "none")

        yield Static(t.t("ui.hub.title") if hasattr(self.app, "i18n") else "Rozcestník", id="hub-title")
        with Grid(id="hub-grid"):
            yield Button(f"{icon('targets', icon_set)} {t.t('ui.hub.targets')}".strip(),
                         id="go-targets",      classes="tile success")
            yield Button(f"{icon('scheduler', icon_set)} {t.t('ui.hub.scheduler')}".strip(),
                         id="go-scheduler",    classes="tile info")
            yield Button(f"{icon('plugins', icon_set)} {t.t('ui.hub.plugins')}".strip(),
                         id="go-plugins",      classes="tile warning")
            yield Button(f"{icon('dictionaries', icon_set)} {t.t('ui.hub.dictionaries')}".strip(),
                         id="go-dictionaries", classes="tile neutral")
            yield Button(f"{icon('settings', icon_set)} {t.t('ui.hub.settings')}".strip(),
                         id="go-settings",     classes="tile danger")
            yield Button(           t.t('ui.hub.sandbox') if hasattr(self.app, "i18n") else "Sandbox",
                         id="go-sandbox",      classes="tile neutral")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        mapping = {
            "go-targets": "targets",
            "go-scheduler": "scheduler",
            "go-plugins": "plugins",
            "go-dictionaries": "dictionaries",
            "go-settings": "settings",
        }
        button_id = event.button.id
        target = mapping.get(button_id) if button_id is not None else None
        if target:
            app = self.app  # type: ignore
            go_method = getattr(app, "go", None)
            if callable(go_method):
                go_method(target)

    async def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            app = self.app  # type: ignore
            go_method = getattr(app, "go", None)
            if callable(go_method):
                go_method("targets")
