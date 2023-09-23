"""
Uses malexport to grab anything I've watched from MAL
https://github.com/seanbreckenridge/malexport
"""

from typing import Optional, Union, List, Callable
from datetime import datetime, date


from malexport.parse.messages import Thread

from promnesia.common import Visit, Loc, Results, iter_urls, logger
from promnesia.sources.html import extract_urls_from_html
from promnesia.sources.markdown import HTML_MARKER


def _msg_from_title(username: str) -> str:
    return f"""<p>MAL message from {username}</p>"""


def _thread_date(tr: Thread) -> Optional[datetime]:
    for m in reversed(tr.messages):
        if m.at:
            return m.at
    return None


def index() -> Results:
    from my.mal.export import anime, manga, posts, threads
    from malexport.parse.combine import AnimeData, MangaData

    min_time = datetime.min.time()

    def _extract_datetime(info: Union[AnimeData, MangaData]) -> Optional[datetime]:
        d: Optional[date] = info.XMLData.finish_date or info.XMLData.start_date
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
                locator=Loc(title=p.title, href=u),
                context=p.body,
            )
        yield Visit(
            url=p.url,
            dt=p.created_at,
            locator=Loc(title=p.title, href=p.url),
            context=p.body,
        )

    for t in threads():
        # NOTE: this aren't real URLs, its pretty difficult to reconstruct the thread id since it requires
        # saving data from every page of the thread individually
        u = f"https://myanimelist.net/mymessages.php?go=read&threadid={t.thread_id}"
        tdt = _thread_date(t)
        if tdt is not None:
            yield Visit(url=u, dt=tdt, locator=Loc(title=t.subject, href=u))

        for m in t.messages:
            if m.at is None:
                logger.debug(f"No date for {m}, ignoring...")
                continue
            subject = f" ({t.subject.strip()})" if t.subject.strip() else ""
            for url, _ in extract_urls_from_html(m.content):
                yield Visit(
                    url=url,
                    dt=m.at,
                    locator=Loc(
                        title=f"MAL Message from {m.username}" + subject, href=u
                    ),
                    context=HTML_MARKER + _msg_from_title(m.username) + m.content,
                )
