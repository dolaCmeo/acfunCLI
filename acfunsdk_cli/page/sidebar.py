# coding=utf-8
from acfunsdk import Acer
from typing import Optional

import click
from rich.markdown import Markdown, ImageItem

from textual import events
from textual.app import App
from textual.driver import Driver
from textual.widgets import Header, Footer, Placeholder, ScrollView
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.pretty import Pretty
from rich import box
from utils.actool import load_image_to_cli


class AcUPSidebar(Placeholder):

    def __init__(self, user_data) -> None:
        self.user = user_data
        super().__init__()

    def up_panel(self):
        avatar = load_image_to_cli(self.user['headUrl'], 32, f"UID:{self.user['id']}")
        up_name_title = Text("UP主", "white on blue")
        name_style = Style(color="white", bgcolor="default")
        ns = self.user["nameStyle"]
        if len(ns) > 7:
            name_style = Style(color=ns[7:], bgcolor="default")
        up_name_title.append(" ", Style(color="white", bgcolor="default"))
        up_name_title.append(self.user['name'], name_style)
        signature = Text(f"{self.user['signature']}", "grey50") if "signature" in self.user else ""
        contribute = Text(f"投稿: {self.user['contributeCountValue']: >14}")
        following = Text(f"关注: {self.user['followingCountValue']: >14}")
        fans = Text(f"粉丝: {self.user['fanCountValue']: >14}")
        return Panel(
            Group(
                Align.center(avatar),
                up_name_title,
                signature,
                contribute,
                following,
                fans,
            ),
            # title=self.__class__.__name__,
            # border_style="green" if self.mouse_over else "blue",
            # box=box.HEAVY if self.has_focus else box.ROUNDED,
            style=self.style,
            height=self.height,
        )

    def render(self):
        return self.up_panel()
