"""
Indexes any links found in my emails
"""

import os
from typing import Set
from datetime import date

from my.core.common import mcachew
from promnesia.common import Results, Visit, Loc, iter_urls, logger
from promnesia.sources.html import extract_urls_from_html


# separated into another non-cachew function so testing is a bit easier
def do_index() -> Results:
    from my.mail.all import mail
    import my.mail.parse_parts as parts_parser

    for m in mail():

        if m.dt is None:
            logger.debug(f"could not parse a date from {m._serialize()}, ignoring...")
            continue

        # mail-specific emitted set, only pull the same URL from one file once
        emitted: Set[str] = set()

        headers_ctx = m.description + "\n\n"

        assert m.filepath is not None

        for payload, content_type in parts_parser.tag_message_subparts(m.message):
            if content_type == parts_parser.EmailText.html:
                for url, text in extract_urls_from_html(payload):
                    if url in emitted:
                        continue
                    # if the URL is the text itself, don't duplicate it
                    ctx = headers_ctx if url == text else headers_ctx + text
                    yield Visit(
                        url=url,
                        dt=m.dt,
                        context=ctx.strip(),
                        locator=Loc.file(m.filepath),
                    )
                    emitted.add(url)
            elif content_type == parts_parser.EmailText.text:
                # iterate line by line, so we can embed a line of the plaintext
                # as context for where this URL was found
                for line in payload.split(os.linesep):
                    lns = line.strip()
                    if lns:
                        for url in iter_urls(line):
                            if url in emitted:
                                continue
                            # if the URL is the entire line, don't duplicate it
                            ctx = headers_ctx if url == lns else headers_ctx + lns
                            yield Visit(
                                url=url,
                                dt=m.dt,
                                context=ctx.strip(),
                                locator=Loc.file(m.filepath),
                            )
                            emitted.add(url)
            else:
                logger.debug(
                    f"Ignoring message part with content type {content_type} from {str(m.filepath)}"
                )


# cache this once every month, it takes about half an hour
@mcachew(depends_on=lambda: date.today().month)
def index() -> Results:
    yield from do_index()
