"""
Extracts links from my todo.txt files
"""

from typing import Set, Tuple

from promnesia.common import Visit, Loc, Results, iter_urls


def index() -> Results:
    from my.todotxt.git_history import events

    emitted: Set[Tuple[str, str]] = set()
    for e in events():
        text = e.todo.bare_description()
        for u in iter_urls(text):
            key = (text, u)
            if key in emitted:
                continue
            yield Visit(
                url=u,
                dt=e.dt,
                context=e.todo.description,
                locator=Loc(title=str(e.todo), href=u),
            )
            emitted.add(key)
