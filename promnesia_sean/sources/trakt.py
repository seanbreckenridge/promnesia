"""
Uses TraktExport to grab anything I've watched from trakt
https://github.com/seanbreckenridge/traktexport
"""

from promnesia.common import Visit, Loc, Results


def index() -> Results:
    from my.trakt.export import history
    from traktexport.dal import Movie, Episode

    for e in history():
        # TODO: filter/fix datetimes from before I created my account?
        # TODO: use SiteIds to expand what this connects to (can link to imdb/moviedb?)
        trakt_url = e.media_data.url
        desc: str
        if isinstance(e.media_data, Movie):
            desc = e.media_data.title
        elif isinstance(e.media_data, Episode):
            # episode
            desc = f"{e.media_data.show.title} - S{e.media_data.season}E{e.media_data.episode} - {e.media_data.title}"
        else:
            yield RuntimeError(f"Unhandled event {repr(e)}")
            continue

        yield Visit(
            url=trakt_url,
            dt=e.watched_at,
            locator=Loc(title=e.media_data.title, href=trakt_url),
            context=desc,
        )
