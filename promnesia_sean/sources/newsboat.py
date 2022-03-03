"""
uses backups of my newsboat subscriptions
to event source when I added/removed subscriptions
"""

from promnesia.common import Results, Visit, Loc


def index() -> Results:
    from my.rss.newsboat.file_backups import events

    for e in events():
        # if I added this as a subscription
        if e.action == "added":
            yield Visit(
                url=e.url, dt=e.dt, locator=Loc(title=f"Added {e.url}", href=e.url)
            )
