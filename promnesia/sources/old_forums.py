"""
Exposes post/metadata from random forums I used in the past
https://github.com/seanbreckenridge/forum_parser
"""

from promnesia.common import Results, Visit, Loc
from promnesia.utils import extract_urls_http


def index() -> Results:
    from my.old_forums import history

    for p in history():
        desc = f"{p.forum_name} - {p.post_title}"
        for url in extract_urls_http(p.post_contents):
            yield Visit(
                url=url,
                dt=p.dt,
                locator=Loc(title=desc, href=p.post_url),
                context=p.post_contents,
            )
