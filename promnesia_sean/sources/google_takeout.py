"""
uses my forked google takeout parser
https://github.com/seanbreckenridge/HPI/tree/master/my/google
"""

from promnesia.common import Visit, Loc, Results


def index() -> Results:
    from my.google import events
    from my.google.models import (
        HtmlComment,
        HtmlEvent,
        LikedVideo,
        AppInstall,
        Location,
    )

    for e in events():
        if isinstance(e, Location):
            continue
        elif isinstance(e, AppInstall):
            continue
        elif isinstance(e, LikedVideo):
            yield Visit(
                url=e.link,
                dt=e.dt,
                context=e.desc,
                locator=Loc(title=e.title, href=e.link),
            )
        elif isinstance(e, HtmlComment):
            for url in e.links:
                # todo: use url_metadata to improve locator?
                # or maybe just extract first sentence?
                yield Visit(
                    url=url,
                    dt=e.dt,
                    context=e.desc,
                    locator=Loc(title=e.desc, href=url),
                )
        elif isinstance(e, HtmlEvent):
            # TODO: regex out title and use it as locator title?
            for url in filter(lambda u: "youtube.com/channel" not in u, e.links):
                yield Visit(
                    url=url,
                    dt=e.dt,
                    context=e.desc,
                    locator=Loc(title=e.desc, href=url),
                )
        else:
            yield RuntimeError(f"Unhandled visit: {repr(e)}")
