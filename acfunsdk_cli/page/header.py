# coding=utf-8
import time
import datetime
from textual import events
from textual.reactive import watch
from textual.widgets import Header
from textual.widget import Widget
from rich.console import RenderableType
from rich.style import Style
from rich.table import Table
from rich.panel import Panel


class AcIndexHeader(Widget):

    def __init__(self) -> None:
        super().__init__()
        self.title = "AcFun弹幕视频网"
        self.layout_size = 1
        self.tall = True
        self.style = Style(color="white", bgcolor="#fd4c5d")

    def __rich_repr__(self):
        yield self.title

    def get_clock(self) -> str:
        return datetime.datetime.now().time().strftime("%X")

    def render(self) -> RenderableType:
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column(justify="left", ratio=0, width=8)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)
        header_table.add_row(
            "AcFan.cn", self.title, self.get_clock()
        )
        header: RenderableType
        header = header_table
        return header

    async def on_mount(self, event: events.Mount) -> None:
        self.set_interval(1.0, callback=self.refresh)

        async def set_title(title: str) -> None:
            self.title = title

        watch(self.app, "title", set_title)


class AcHeader(Header):
    def __init__(
        self,
        *,
        ac_raw: dict
    ) -> None:
        super().__init__()
        self.tall = True
        self.style = Style(color="white", bgcolor="#fd4c5d")
        self.clock = True
        self.ac_raw = ac_raw

    @property
    def full_title(self) -> str:
        return f"{self.title}\n{self.ac_info}"

    @property
    def ac_info(self) -> str:
        # infos = [
        #     f"👁{self.ac_raw['viewCount']}",
        #     f"💕{self.ac_raw['likeCount']}",
        #     f"⭐{self.ac_raw['stowCount']}",
        #     f"🍌{self.ac_raw['bananaCount']}",
        #     f"📧{self.ac_raw['shareCount']}",
        # ]
        infos = [
            f"看{self.ac_raw['viewCount']}",
            f"赞{self.ac_raw['likeCount']}",
            f"藏{self.ac_raw['stowCount']}",
            f"蕉{self.ac_raw['bananaCount']}",
            f"享{self.ac_raw['shareCount']}",
        ]
        return " ".join(infos)

    @property
    def channel_info(self) -> str:
        channel = f"{self.ac_raw['channel']['parentName']}>>{self.ac_raw['channel']['name']}"
        unix = self.ac_raw.get("createTimeMillis", time.time() * 1000)
        date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix // 1000))
        return "\n".join([channel, date_str])

    async def watch_tall(self, tall: bool) -> None:
        self.layout_size = 4 if tall else 1

    def render(self) -> RenderableType:
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column("channel", justify="left", ratio=0, width=12)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)
        header_table.add_row(
            self.channel_info, self.full_title, self.get_clock() if self.clock else ""
        )
        header: RenderableType
        header = Panel(header_table, style=self.style) if self.tall else header_table
        return header
