# coding=utf-8
from utils.actool import load_image_to_cli
from rich.style import Style
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.console import Group
from rich.panel import Panel


class AcIndexPage:
    def __init__(self, acer, width: int = 120):
        self.acer = acer
        self.index_obj = self.acer.acfun.AcIndex()
        self.window_width = width
        self.style = Style(color="white", bgcolor="#fd4c5d")
        pass

    def _gen_banner(self, layout: Layout):
        banner = self.index_obj.get("banner")
        title = Text(banner['title'])
        title.stylize(Style(link=banner['url']))
        banner_img = load_image_to_cli(banner['image'], self.window_width, title)
        layout['banner'].update(banner_img)

    def _gen_table_item(self, data: dict, table_title: str):
        table = Table.grid(expand=True)
        table.add_column("num", justify="right", ratio=0, width=3)
        table.add_column("title", justify="left")
        for i, item in enumerate(data):
            text = Text(item["title"], justify="left", overflow="ellipsis", no_wrap=True)
            text.stylize(Style(link=item.get("url") or item.get("link")))
            table.add_row(f"{(i + 1): >2} ", text)
        return Group(
            Text(table_title, style=self.style),
            table
        )

    def _gen_top_area(self, layout: Layout):
        top_area = self.index_obj.get("top_area")
        layout['top_area'].split_row(
            Layout(name="slider"),
            Layout(name="items")
        )
        layout["slider"].update(self._gen_table_item(top_area['slider'], "  轮播图  "))
        layout["items"].update(self._gen_table_item(top_area['items'], "  置顶区  "))

    def page(self):
        area = Layout()
        area.split_column(
            Layout(name="banner", size=6),
            Layout(name="top_area", size=7),
        )
        self._gen_banner(area)
        self._gen_top_area(area)
        return area
