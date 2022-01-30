"""
Uses malexport to grab anything I've watched from MAL
https://github.com/seanbreckenridge/malexport
"""

from typing import Optional, Union, List, Callable
from datetime import datetime, date

from promnesia.common import Visit, Loc, Results, iter_urls


def index() -> Results:
    from my.mal.export import anime, manga, posts
    from malexport.parse.combine import AnimeData, MangaData

    min_time = datetime.min.time()

    def _extract_datetime(info: Union[AnimeData, MangaData]) -> Optional[datetime]:
        d: Optional[date] = info.XMLData.finish_date or info.XMLData.start_date
        dt: datetime
        if d is not None:
            return datetime.combine(d, min_time)
        else:
            if len(info.history) > 0:
                return info.history[0].at
        return None

    funcs: List[Callable[[], Union[AnimeData, MangaData]]] = [anime, manga]  # type: ignore[list-item]
    for _type, func in zip(["anime", "manga"], funcs):
        for item in func():
            assert isinstance(item, AnimeData) or isinstance(item, MangaData)
            dt: Optional[datetime] = _extract_datetime(item)
            if dt is None:
                continue

            # append both the URL with the metadata in the URL
            # and the one without
            urls = [f"https://myanimelist.net/{_type}/{item.id}"]
            if item.JSONList is not None and item.JSONList.url is not None:
                urls.append(item.JSONList.url)
            for u in urls:
                yield Visit(
                    url=u,
                    dt=dt,
                    locator=Loc(title=item.XMLData.title, href=u),
                    context=item.XMLData.title,
                )

    for p in posts():
        for u in iter_urls(p.body):
            yield Visit(
                url=u,
                dt=p.created_at,
                locator=Loc(title=p.title, href=f"MyAnimeList - {p.title}"),
                context=p.body,
            )
        yield Visit(
            url=p.url,
            dt=p.created_at,
            locator=Loc(title=p.title, href=f"MyAnimeList {u.title}"),
            context=p.body,
        )
