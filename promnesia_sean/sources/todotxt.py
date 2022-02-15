"""
Extracts links from my todo.txt files
"""

from typing import Set, Tuple

from promnesia.common import Visit, Loc, Results, iter_urls


def index() -> Results:
    from my.todotxt.file_backups import events

    emitted: Set[Tuple[str, str]] = set()
    for e in events():
        for u in iter_urls(e.todo.description):
            key = (e.todo.description, u)
            if key in emitted:
                continue
            yield Visit(
                url=u,
                dt=e.dt,
                context=e.todo.description,
                locator=Loc(title=e.todo.description, href=u),
            )
            emitted.add(key)
