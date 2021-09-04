"""
Indexes any links I sent in discord messages
"""

from promnesia.common import Results, Visit, Loc, iter_urls


def index(*, render_markdown: bool = False) -> Results:
    from my.discord import messages

    # TODO: optionally import? this would break if someone
    # hasnt installed promnesia like pip3 install '.[all]' to
    # to install the markdown module for promnesia
    from promnesia.sources.markdown import TextParser

    for m in messages():
        # hmm - extract URLs from attachments?
        # Probably not very useful unless I extract info from them with url_metadata or something

        context: str = m.content

        # if render_markdown flag is enabled, render the text as markdown (HTML)
        if render_markdown:
            context = TextParser(m.content)._doc_ashtml()

        # permalink back to this discord message
        loc = Loc.make(title=m.channel.description, href=m.link)

        for u in iter_urls(m.content):
            yield Visit(
                url=u,
                dt=m.timestamp,
                context=context,
                locator=loc,
            )
