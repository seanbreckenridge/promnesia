"""
uses backups of my newsboat subscriptions
to event source when I added/removed subscriptions
"""

from promnesia.common import Results, Visit, Loc


def index() -> Results:
    from my.newsboat import events

    for e in events():
        # if I added this as a subscription
        if e.added:
            yield Visit(
                url=e.url, dt=e.dt, locator=Loc(title=f"Added {e.url}", href=e.url)
            )
