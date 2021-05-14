"""
Extracts links from my bash history
"""

from promnesia.common import Visit, Loc, Results, iter_urls


def index() -> Results:
    from my.bash import history

    for e in history():
        for u in iter_urls(e.command):
            yield Visit(
                url=u,
                dt=e.dt,
                context=e.command,
                locator=Loc(title=e.command, href=u),
            )
