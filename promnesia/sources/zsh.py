"""
Extracts links from my zsh history
"""

from promnesia.common import Visit, Loc, Results
from promnesia.utils import extract_urls_http


def index() -> Results:
    from my.zsh import history

    for e in history():
        for u in extract_urls_http(e.command):
            yield Visit(
                url=u,
                dt=e.dt,
                context=e.command,
                locator=Loc(title=f"zsh: {e.command}", href=u),
                duration=e.duration,
            )
