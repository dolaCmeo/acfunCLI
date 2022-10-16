# coding=utf-8
from typing import Optional

from acfunsdk import Acer
from textual import events
from textual.app import App
from page.header import AcIndexHeader
from page.footer import AcIndexFooter
from page.index import AcIndexPage
from textual.widgets import ScrollView
from rich.console import Console
from textual.reactive import Reactive

console = Console()


class AcIndex(App):

    def __init__(self, **kwargs):
        super().__init__(title="AcFun弹幕视频网", **kwargs)
        self.acer = Acer()

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("a", "view.toggle('sidebar')", "栏目")
        await self.bind("f5", "refresh", "刷新")
        await self.bind("escape", "quit", "退出")

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""

        # A scrollview to contain the markdown file
        body = ScrollView(gutter=1)

        # Header / footer / dock
        await self.view.dock(AcIndexHeader(), edge="top")
        await self.view.dock(AcIndexFooter(), edge="bottom")
        # await self.view.dock(AcUPSidebar(up_data), edge="left", size=30, name="sidebar")

        # Dock the body in the remaining space
        await self.view.dock(body, edge="right", name="index")

        async def get_index():
            index_obj = AcIndexPage(self.acer, self.console.width)
            page = index_obj.page()
            await body.update(page)

        await self.call_later(get_index)

    pass


# index_obj = AcIndexPage(Acer(), console.width - 30)
# page = index_obj.page()
# console.print(page)
AcIndex.run(log="textual.log")
