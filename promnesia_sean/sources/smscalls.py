"""
Extracts links from sms messages
Exported using https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en_US
"""

from promnesia.common import Visit, Loc, Results, iter_urls


def index() -> Results:
    from my.smscalls import messages

    for m in messages():
        for u in iter_urls(m.message):
            yield Visit(
                url=u,
                dt=m.dt,
                context=m.message,
                locator=Loc(title=f"Message with {m.who} ({m.phone_number})"),
            )
