"""
Export any links in git commit messages
"""

from promnesia.common import Results, Visit, Loc, iter_urls


def index() -> Results:
    from my.coding.commits import commits

    for c in commits():
        for url in iter_urls(c.message):
            desc = f"{c.repo}\n{c.message}"
            yield Visit(
                url=url,
                dt=c.committed_dt,
                context=desc,
                locator=Loc(title=f"{c.repo} {c.sha}", href=c.repo),
            )
