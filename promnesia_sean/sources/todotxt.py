"""
Extracts links from my todo.txt files
"""

from typing import Set, Tuple

from promnesia.common import Visit, Loc, Results
from ..utils import extract_urls_http


def index() -> Results:
    from my.todotxt import events

    emitted: Set[Tuple[str, str]] = set()
    for e in events():
        for u in extract_urls_http(e.todo.text):
            key = (e.todo.text, u)
            if key in emitted:
                continue
            yield Visit(
                url=u,
                dt=e.dt,
                context=e.todo.text,
                locator=Loc(title=e.todo.text, href=u),
            )
            emitted.add(key)
