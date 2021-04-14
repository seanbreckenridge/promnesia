"""
Extracts links from ttt -- an extension to my shell history
https://github.com/seanbreckenridge/ttt
"""

from promnesia.common import Visit, Loc, Results
from ..utils import extract_urls_http


def index() -> Results:
    from my.ttt import history

    for e in history():
        for u in extract_urls_http(e.command):
            yield Visit(
                url=u,
                dt=e.dt,
                context=e.command,
                locator=Loc(title=e.command, href=u),
            )
