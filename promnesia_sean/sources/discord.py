"""
Indexes any links I sent in discord messages
"""

from promnesia.common import Results, Visit, Loc, extract_urls

BASE = "https://discord.com"


def index() -> Results:
    from my.discord import messages

    for m in messages():
        # hmm - extract URLs from attachments?
        # Probably not very useful unless I extract info from them with url_metadata or something
        for u in extract_urls(m.content):
            yield Visit(
                url=u,
                dt=m.timestamp,
                context=m.content,
                locator=Loc(title=m.channel.description, href=m.link),
            )
