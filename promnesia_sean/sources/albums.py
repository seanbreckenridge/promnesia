"""
Any albums I've listened to
https://github.com/seanbreckenridge/albums
"""

from datetime import datetime

from promnesia.common import Visit, Loc, Results


def index() -> Results:
    from my.albums import history

    for a in history():
        if a.discogs_url is not None and a.listened_on is not None:
            dt = datetime.combine(a.listened_on, datetime.min.time())
            title = f"{a.album_name} - {a.cover_artists}"
            # TODO: add stringified description of album as context?
            yield Visit(
                url=a.discogs_url,
                dt=dt,
                locator=Loc(title=title, href=a.discogs_url),
            )
