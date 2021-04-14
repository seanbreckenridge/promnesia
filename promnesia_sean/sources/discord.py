"""
Indexes any links I sent in discord messages
"""

from promnesia.common import Results, Visit, Loc
from ..utils import extract_urls_http

BASE = "https://discord.com"


def index() -> Results:
    from my.discord import messages

    for m in messages():
        # extract any URLs from content
        # hmm - extract URLs from attachments.
        # Probably not very useful unless I extract info from them with url_metadata or something
        urls = extract_urls_http(m.content)

        if len(urls) == 0:
            continue

        cid = m.channel.channel_id
        # no server info, probably a PM
        if m.channel.server is None:
            desc = m.channel.name or f"message ({cid})"
            link = f"{BASE}/channels/@me/{cid}/{m.message_id}"
        else:
            s = m.channel.server
            # has a server object, in a server
            desc = f"{s.server_name} - #{m.channel.name}"
            link = f"{BASE}/channels/{s.server_id}/{cid}/{m.message_id}"

        for u in urls:
            yield Visit(
                url=u,
                dt=m.timestamp,
                context=m.content,
                locator=Loc(title=desc, href=link),
            )
