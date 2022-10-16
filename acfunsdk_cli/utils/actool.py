# coding=utf-8
import os
import time
import httpx
from io import BytesIO
from PIL import Image
from .climage import _toAnsi
from .climage import _color_types
from bs4 import BeautifulSoup as Bs
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from rich.progress import Progress
from rich.align import Align
from rich.live import Live
from rich.prompt import Prompt

__author__ = 'dolacmeo'

header = {
    # "Referer": "https://www.acfun.cn/",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.102 Safari/537.36'
}


def trans_article_to_markdown(content: str):
    markdown_text = ""
    if content.startswith("<div>") and content.endswith("</div>"):
        content = content[5:-6]
    content = content.replace("\t", "")
    html_obj = Bs(content, "lxml")
    tags = html_obj.select("div,p,hr,ol")
    for tag in tags:
        if tag.name == "hr":
            markdown_text += "- - -\n"
            continue
        for t in tag:
            if t.name is None:
                markdown_text += t.text
            elif t.name == "img":
                t.src = Bs(str(t), "lxml").select_one("img").attrs['src']
                markdown_text += f"![acfun-img]({t.src})"
            elif t.name == "strong":
                markdown_text += f"**{t.text}**"
            elif t.name == "em":
                markdown_text += f"*{t.text}*"
            elif t.name == "li" and tag.name == "ol":
                markdown_text += f"+ {t.text}"
            elif t.name == "br":
                markdown_text += "\n"
            markdown_text += "\n"
        markdown_text += "\n"
    return markdown_text


def load_image_to_cli(url_or_path, max_width, title=None):
    ansi_rate = 1.3
    width = min(int(max_width or 100), max_width - 10)  # 最大不超过窗口宽
    # _max_height = min(int(width / ansi_rate), console.height - 10)  # 最大高不超出窗口高
    if os.path.isfile(url_or_path):
        _im = Image.open(url_or_path).convert('RGB')
    else:
        req = httpx.get(url_or_path, headers=header)
        _im = Image.open(BytesIO(req.content)).convert('RGB')
        req.close()
    i_width, i_height = _im.size
    _im = _im.resize((int(i_width * ansi_rate), i_height))  # 拉伸消除变形
    if i_width <= 128:
        width = width // 4
        # _max_height = _max_height // 4
    if _im.size[0] != width:  # 定宽 调高
        i_width, i_height = _im.size
        new_h = int(width / i_width * i_height)
        _im = _im.resize((width, new_h), Image.ANTIALIAS)
    # if _im.size[1] > _max_height:  # 超限高调整
    #     i_width, i_height = _im.size
    #     new_w = int(_max_height / i_height * i_width)
    #     _im = _im.resize((new_w, _max_height), Image.ANTIALIAS)
    _ansi = _toAnsi(_im, oWidth=_im.size[0], is_unicode=True,
                    color_type=_color_types.truecolor, palette="default")
    txt_h = _ansi.count("\n")
    _txt = Text.from_ansi(_ansi)
    return Panel(_txt, subtitle=title, subtitle_align='center', width=_im.size[0] + 4, height=txt_h + 2)


def video_thumbnails(path, text_width: int = 160, title: str = ""):
    # 视频预览图，横向100区块分割
    text_width -= 4
    text_width = max(text_width, 114)
    ansi_rate = 1.3
    _im = Image.open(path).convert('RGB')
    i_width, i_height = _im.size
    p_width = i_width // 100
    text_width = min(text_width, p_width)
    vv = 4 if i_height > p_width else 1
    text_height = int(text_width / p_width * i_height)
    thumbnails = list()
    with Progress() as progress:
        task1 = progress.add_task("loading thumbnails", total=100)
        for i in range(100):
            region = _im.crop((i * p_width, 0, (i + 1) * p_width, i_height))
            region = region.resize((text_width, text_height), Image.Resampling.LANCZOS)
            region = region.resize((text_width, int(text_height // ansi_rate)))  # 拉伸消除变形
            _ansi = _toAnsi(region, oWidth=text_width // vv, is_unicode=True,
                            color_type=_color_types.truecolor, palette="default")
            _txt = Text.from_ansi(_ansi)
            ii = i + 1
            progress_text = "▶ " if ii < 100 else "■ "
            progress_text += f"{ii: >3}/100 |"
            progress_text += "[red]=[/red]" * i
            progress_text += "[red]>[/red]"
            progress_text += "-" * (100 - ii)
            progress_text += "|"
            panel = Panel(Align(_txt, "center"),
                          title=title, title_align="left",
                          subtitle=progress_text, subtitle_align="center",
                          width=text_width + 4)
            thumbnails.append(panel)
            progress.update(task1, advance=1)
    return thumbnails


def play_thumbnails(path) -> None:
    console = Console()
    console.clear()
    if console.width < 118 or console.height < 28:
        console.print(f"窗口太小了~ (宽度:{console.width}<118,高度:{console.height}<28)")
        return
    thumbnails = video_thumbnails(path, console.width)

    def play():
        console.clear()
        with Live() as live:
            for i, p in enumerate(thumbnails):
                live.update(Align(p, align="center", vertical="middle"))
                if i < 2:
                    time.sleep(0.4)
                elif i % 2 == 0:
                    time.sleep(0.2)
                else:
                    time.sleep(0.1)
        console.print(f"播放完毕咯~")
    play()
    cmd = "ask"
    while cmd != "quit":
        cmd = Prompt.ask(r"回车退出, \[r] 重放", choices=["r", "R", "quit"], default="quit")
        if cmd.lower() == "r":
            play()
    console.clear()
    return


if __name__ == '__main__':
    img = r"D:\AcSaver\video\37536001\data\37536001.thumbnails.png"
    play_thumbnails(img)
