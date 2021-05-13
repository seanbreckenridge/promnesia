"""
Pageview history from the twitch privacy export
https://github.com/seanbreckenridge/HPI/blob/master/my/twitch/gdpr.py
https://www.twitch.tv/p/en/legal/privacy-choices/#user-privacy-requests
"""

from promnesia.common import Visit, Loc, Results


def index() -> Results:
    from my.twitch.gdpr import events

    for e in events():
        if e.event_type == "pageview":
            url = str(e.context)
            yield Visit(
                url=url,
                dt=e.dt,
                locator=Loc.make(title=f"Twitch {e.context}", href=url),
            )
