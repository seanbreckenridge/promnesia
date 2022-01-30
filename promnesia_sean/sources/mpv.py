"""
uses my history daemon to track
any videos/podcasts I've listened to through mpv
https://github.com/seanbreckenridge/mpv-history-daemon
"""
from promnesia.common import Visit, Loc, Results


def index() -> Results:
    from my.mpv.history_daemon import history

    for play in history():
        if play.is_stream:
            url = play.path
            yield Visit(
                url=url,
                dt=play.start_time,
                duration=int(play.listen_time),
                locator=Loc(title=play.media_title or play.path, href=url),
            )
