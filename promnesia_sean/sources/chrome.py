"""
chrome history -- from my HPI module, but parsed using promnesia
its included in HPI module just to expose the info there incase
I want to use it -- and to make configuraton/backups easier
see https://github.com/seanbreckenridge/HPI/blob/master/my/chrome.py
"""

from promnesia.common import Results


def index() -> Results:
    from my.chrome import history

    # already promnesia visits
    yield from history()
