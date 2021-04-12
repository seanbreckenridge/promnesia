from promnesia.common import Results, Visit, Loc, extract_urls


def index() -> Results:
    from my.discord import messages

    for m in messages():
        text = m.content
        urls = extract_urls(text)
        if len(urls) == 0:
            continue
        # todo:b href?
        loc = Loc.make(title=f"message in {m.channel.name} - {m.channel.server_name}")

        for u in urls:
            yield Visit(url=u, dt=m.timestamp, context=text, locator=loc)
