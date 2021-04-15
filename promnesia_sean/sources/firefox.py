"""
firefox export - my browsing history
https://github.com/seanbreckenridge/ffexport
"""

from promnesia.common import Results, Visit, Loc


def index() -> Results:
    from my.firefox import history

    for v in history():
        yield Visit(
            url=v.url,
            dt=v.visit_date,
            locator=Loc(title=v.title or f"Firefox - {v.url}", href=v.url),
        )
