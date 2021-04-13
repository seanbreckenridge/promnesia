"""
Exposes post/metadata from random forums I used in the past
https://github.com/seanbreckenridge/forum_parser
"""

from promnesia.common import Results, Visit, Loc, extract_urls


def index() -> Results:
    from my.old_forums import history

    for post in history():
        for url in extract_urls(post.post_contents):
            yield Visit(
                url=url,
                dt=post.dt,
                locator=Loc(
                    title=f"{post.forum_name} - {post.post_title}", href=post.post_url
                ),
                context=post.post_contents,
            )
