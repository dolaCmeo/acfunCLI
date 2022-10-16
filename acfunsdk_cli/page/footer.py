# coding=utf-8
from textual.widgets import Footer
from rich.style import Style
from rich.text import Text
from rich.table import Table


class AcIndexFooter(Footer):

    style = Style(color="white", bgcolor="#fd4c5d")

    def make_key_text(self):
        """Create text containing all the keys."""
        footer_table = Table.grid(padding=(0, 1), expand=True)
        footer_table.style = self.style
        footer_table.add_column("keys", justify="left", ratio=0)
        footer_table.add_column("user", justify="right")
        text = Text(
            style=self.style,
            no_wrap=True,
            overflow="ellipsis",
            justify="left",
            end="",
        )
        for binding in self.app.bindings.shown_keys:
            key_display = (
                binding.key.upper()
                if binding.key_display is None
                else binding.key_display
            )
            hovered = self.highlight_key == binding.key
            key_text = Text.assemble(
                (f" {key_display} ", "reverse" if hovered else "default on default"),
                f" {binding.description} ",
                meta={"@click": f"app.press('{binding.key}')", "key": binding.key},
            )
            text.append_text(key_text)
        acer_login = Text(style=self.style, no_wrap=True, overflow="ellipsis", justify="right", end="")
        acer_login.append_text(Text.assemble(
            (f" 未登录 ", "reverse" if self.highlight_key == "u" else "default on default"),
            meta={"@click": f"app.press('u')", "key": 'u'},
        ))
        footer_table.add_row(text, acer_login)
        return footer_table
