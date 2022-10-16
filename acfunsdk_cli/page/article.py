# coding=utf-8
import click
from utils.actool import trans_article_to_markdown, load_image_to_cli
from page.sidebar import AcUPSidebar
from page.header import AcHeader
from rich.markdown import Markdown, ImageItem

from textual import events
from textual.app import App
from textual.driver import Driver
from textual.widgets import Header, Footer, Placeholder, ScrollView
from rich.text import Text
from rich.style import Style

from acfunsdk import Acer

content = "INIT FIRST"
title = "undefined"
raw_data = dict()
up_data = dict()


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
        await self.view.dock(AcHeader(ac_raw=raw_data), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(AcUPSidebar(up_data), edge="left", size=30, name="sidebar")

        # Dock the body in the remaining space
        await self.view.dock(body, edge="right")

        async def get_markdown() -> None:
            text = trans_article_to_markdown(content['content'])
            md = Markdown(text, hyperlinks=True)
            md.elements['image'] = AcImageItem
            await body.update(md)
            self.title = title

        await self.call_later(get_markdown)


@click.command()
@click.argument('src')
def main(src):
    acer = Acer()
    obj = acer.get(src)
    if obj is None:
        return None
    global content, title, raw_data, up_data
    raw_data = obj.raw_data
    content = obj.contents[0]
    title = obj.title
    up_data = obj.raw_data['user']
    # MyApp.run(title="Simple App", log="textual.log")
    MyApp.run(title="Simple App")


if __name__ == '__main__':
    main()
