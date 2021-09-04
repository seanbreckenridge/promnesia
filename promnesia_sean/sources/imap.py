"""
Indexes any links found in my emails
"""

from typing import Set, List

from promnesia.common import Results, Visit, Loc, iter_urls


def parse_person(m: List[List[str]]):
    """
    e.g.:
    [
        [
            "",
            "emailhere@gmail.com"
        ]
    ]
    """
    if m:
        if m[0]:
            return m[0][1]


def index() -> Results:
    from my.imap import mail

    for m in mail():
        emitted: Set[str] = set()
        desc = f"""{parse_person(m.from_)} {parse_person(m.to)} - {m.subject}"""

        for body in (
            m.body,
            m.body_plain,
            m.body_html,
        ):
            for url in iter_urls(body):
                if url in emitted:
                    continue
                emitted.add(url)
                yield Visit(
                    url=url, dt=m.date, context=body, locator=Loc(title=desc, href=url)
                )
