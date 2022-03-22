"""
Indexes any links found in my emails
"""

import os
from typing import Set, List, Iterator, Tuple
from datetime import date
from email.message import Message

from my.core.common import mcachew
from promnesia.common import Results, Visit, Loc, iter_urls, logger
from promnesia.sources.html import extract_urls_from_html

# explicity ignored types, anything else sends a warning
IGNORED_CONTENT_TYPES = set(
    [
        "text/calendar",
        "application/ics",
        "application/pdf",
        "application/octet-stream",
        "application/octetstream",
        "text/csv",
        "application/json",
        "application/zip",
        "application/x-zip-compressed",
        "application/msword",
        "multipart/alternative",
        "application/postscript",
        "text/x-vcard",
        "multipart/parallel",  # not sure what the best way to parse this is
    ]
)

IGNORED_CONTENT_PREFIXES = set(
    [
        "application/vnd",
        "application/x-apple",
        "application/x-iwork",
        "image",
        "audio",
        "video",
    ]
)


def describe_person(p: Tuple[str, str]) -> str:
    """
    (
        "Person",
        "emailhere@gmail.com"
    )
    converts to
    Person <emailhere@gmail.com>
    if theres no 'Person' text, it
    just becomes:
    emailhere@gmail.com
    """
    if p[0].strip():
        return f"{p[0]} <{p[1]}>"
    else:
        return p[1]


def describe_persons(m: List[Tuple[str, str]]) -> str:
    """
    >>> [('Google', 'no-reply@accounts.google.com'), ('Github', 'no-reply@github.com')]
    'Google <no-reply@accounts.google.com>, Github <no-reply@github.com>'
    """
    return ", ".join([describe_person(p) for p in m])


def _get_msg_subparts(m: Message) -> Iterator[Message]:
    # since walk returns both multiparts and their children
    # we can ignore the multipart and return all individual parts
    #
    # if single type, it just returns the message itself
    for part in m.walk():
        if not part.is_multipart():
            yield part


# separated into another non-cachew function so testing is a bit easier
def do_index() -> Results:
    from my.mail.all import mail

    # if mechanism to remove duplicate messages isn't working because
    # of differing formats, let the user specify the raw_mail function

    for m in mail():

        if m.dt is None:
            logger.debug(f"could not parse a date from {m._serialize()}, ignoring...")
            continue

        # mail-specific emitted set, only pull the same URL from one file once
        emitted: Set[str] = set()

        headers_ctx = f"""From: {describe_persons(m.from_)}
To: {describe_persons(m.to)}
Subject: {m.subject}

"""

        assert m.filepath is not None

        for message_part in _get_msg_subparts(m.message):
            content_type = message_part.get_content_type()
            payload = message_part.get_payload()

            if content_type in IGNORED_CONTENT_TYPES:
                continue

            if any(
                [content_type.startswith(prefix) for prefix in IGNORED_CONTENT_PREFIXES]
            ):
                continue

            if content_type.startswith("text") and "html" in content_type:
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

            elif content_type == "text/plain":
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
