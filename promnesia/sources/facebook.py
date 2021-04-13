"""
Extracts links from my faceook GDPR export
https://github.com/seanbreckenridge/HPI/tree/master/my/facebook.py
"""

from promnesia.common import Visit, Loc, Results
from promnesia.utils import extract_urls_http


def index() -> Results:
    from my.facebook import events
    from my.facebook import (
        Post,
        Comment,
        Conversation,
    )

    for e in events():
        if isinstance(e, Exception):
            yield e
            continue
        elif isinstance(e, Post):
            for url in extract_urls_http(e.content):
                yield Visit(
                    url=url,
                    dt=e.dt,
                    locator=Loc(title=e.action or ""),
                    context=e.content,
                )
        elif isinstance(e, Conversation):
            for msg in e.messages:
                for url in extract_urls_http(msg.content):
                    yield Visit(
                        url=url,
                        dt=msg.dt,
                        context=msg.content,
                        locator=Loc(title=msg.author),
                    )
        else:
            # ignore other events
            continue
