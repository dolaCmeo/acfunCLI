# coding=utf-8
import click
from utils.actool import video_thumbnails
from page.sidebar import AcUPSidebar
from rich.markdown import Markdown, ImageItem

from textual import events
from textual.app import App
from textual.driver import Driver
from textual.widgets import Header, Footer, Placeholder, ScrollView
from rich.text import Text
from rich.style import Style
from rich.panel import Panel

from acfunsdk import Acer

title = "undefined"
up_data = dict()
thumbnails = list()


class AcImageItem(ImageItem):

    def __rich_console__(self, console, options):
        title = self.text or Text(self.destination.strip("/").rsplit("/", 1)[-1])
        title.stylize(Style(link=self.link or self.destination or None))
        img = load_image_to_cli(self.link or self.destination, console.width - 30, title)
        yield img


class MyApp(App):
    """An example of a very simple Textual App"""

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("a", "view.toggle('sidebar')", "UP主")
        await self.bind("q", "quit", "退出")
        await self.bind("escape", "quit", "退出")

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""

        # A scrollview to contain the markdown file
        body = ScrollView(gutter=1)

        # Header / footer / dock
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(AcUPSidebar(up_data), edge="left", size=30, name="sidebar")

        # Dock the body in the remaining space
        await self.view.dock(body, edge="right")

        async def play_video() -> None:
            self.title = title
            for x in thumbnails:
                await body.update(Panel(x))

        await self.call_later(play_video)


@click.command()
@click.argument('src')
def main(src):
    acer = Acer()
    obj = acer.get(src)
    if obj is None:
        return None
    global title, up_data, thumbnails
    title = obj.title
    up_data = obj.raw_data['user']
    thumbnails = video_thumbnails(r"D:\Project\acfunsdk-cli\acfunsdk_cli\page\15244744.thumbnails.png")
    MyApp.run(title="Simple App")


if __name__ == '__main__':
    main()
