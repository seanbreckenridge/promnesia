"""
Uses https://github.com/seanbreckenridge/google_takeout_parser
"""

from promnesia.common import Visit, Loc, Results


def index() -> Results:
    from my.google_takeout import events
    from google_takeout_parser.models import Activity, YoutubeComment, LikedYoutubeVideo

    for e in events():
        if isinstance(e, LikedYoutubeVideo):
            yield Visit(url=e.link, dt=e.dt, context=e.desc, locator=Loc(title=e.title))
        elif isinstance(e, YoutubeComment):
            for url in e.urls:
                # todo: use url_metadata to improve locator?
                # or maybe just extract first sentence?
                yield Visit(
                    url=url, dt=e.dt, context=e.content, locator=Loc(title=e.content)
                )
        elif isinstance(e, Activity):
            # TODO: regex out title and use it as locator title?
            if e.titleUrl is not None:
                yield Visit(
                    context=e.header,
                    url=e.titleUrl,
                    dt=e.time,
                    locator=Loc(title=e.title),
                )
            for s in e.subtitles:
                if s[1] is not None:
                    if "youtube.com/channel" in s[1]:
                        continue
                    yield Visit(
                        url=s[1], context=s[0], dt=e.time, locator=Loc(title=e.title)
                    )
