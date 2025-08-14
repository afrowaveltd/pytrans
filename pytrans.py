import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from services.settings_service import Settings
from services.localization_service import LocalizationService

class PyTransApp(App):
    t = LocalizationService(Settings().get("language", "en"))
    def __init__(self):
        self.settings = Settings()
        

    def compose(self) -> ComposeResult:
        yield Header(show_clock = True)
        yield Footer()

if __name__ == "__main__":
    app = PyTransApp()
    #app.run()
    print(get("Application starting"))