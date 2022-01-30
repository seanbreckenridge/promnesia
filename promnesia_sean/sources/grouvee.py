"""
Uses Grouvee CSV export data
https://github.com/seanbreckenridge/grouvee_export
"""

from promnesia.common import Visit, Loc, Results


def index() -> Results:
    from my.grouvee.export import games

    for g in games():
        game_url = g.url
        loc = Loc.make(title=f"Grouvee {g.name}", href=game_url)
        for s in g.shelves:
            yield Visit(
                url=game_url, dt=s.added, locator=loc, context=f"{g.name} ({s.name})"
            )
