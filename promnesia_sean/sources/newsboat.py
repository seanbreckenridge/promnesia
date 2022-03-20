"""
uses backups of my newsboat subscriptions
to event source when I added/removed subscriptions
"""

from datetime import datetime
from promnesia.common import Results, Visit, Loc, iter_urls


def index() -> Results:
    from my.rss.newsboat.git_history import events

    for e in events():
        # if I added this as a subscription
        if e.action == "added":
            for u in iter_urls(e.data):
                yield Visit(
                    url=u,
                    dt=datetime.fromtimestamp(e.epoch_time),
                    locator=Loc(title=f"Added {u}", href=u),
                )
