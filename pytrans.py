import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from services.settings_service import Settings
from services.localization_service import LocalizationService

class PyTransApp(App):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.t = LocalizationService(self.settings.language)  # or Settings().get("language","en")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

    async def on_mount(self) -> None:
        self.log(self.t.get("Application starting"))

if __name__ == "__main__":
    PyTransApp().run()