"""
Extracts links from my ipython history
"""

from promnesia.common import Visit, Loc, Results, iter_urls, logger


def index() -> Results:
    from my.ipython import history

    for e in history():
        if isinstance(e, Exception):
            logger.exception(e)
            continue
        for u in iter_urls(e.command):
            yield Visit(
                url=u,
                dt=e.dt,
                context=e.command,
                locator=Loc(title=e.command, href=u),
            )
