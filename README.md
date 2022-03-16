## promnesia

This lets me use [my own HPI modules](https://github.com/seanbreckenridge/HPI) as additional `Source`s for [promnesia](https://github.com/karlicoss/promnesia).

It indexes any URLs it finds in my:

- Discord messages, [parsed from the data export](https://github.com/seanbreckenridge/discord_data)
- Browser history from backups of my firefox/chrome/safari browser histories (using [browserexport](https://github.com/seanbreckenridge/browserexport))
- Podcasts/Videos I watched with mpv (tracked by [this](https://github.com/seanbreckenridge/mpv-history-daemon))
- Youtube videos/comments parsed by [google_takeout_parser](https://github.com/seanbreckenridge/google_takeout_parser) from my [google takeout](https://takeout.google.com/)
- Movies/TV Show episodes tracked by my [trakt](https://github.com/seanbreckenridge/traktexport)
- Anime/Manga using [malexport](https://github.com/seanbreckenridge/malexport)
- Shell histories (zsh, bash, ipython, [ttt](https://github.com/seanbreckenridge/ttt))
- Git commits on my system
- Todo.txt files
- Mail, using local IMAP backups
- Albums [I've listened to](https://sean.fish/s/albums)
- Facebook Messages
- comments from some [old forums](https://github.com/seanbreckenridge/forum_parser) I used to be on
- pageview history from the [twitch privacy export](https://github.com/seanbreckenridge/HPI/blob/master/my/twitch/gdpr.py)
- video games I've logged to [grouvee](https://www.grouvee.com/), using [grouvee export](https://github.com/seanbreckenridge/grouvee_export)

[My Promnesia config file](https://sean.fish/d/promnesia/config.py?dark)

### Install

For the time being, this doesn't install as a namespace package alongside `promnesia`, it just installs a separate module, `promnesia_sean`. See the comments [here](https://github.com/karlicoss/promnesia/pull/225) for more info.

To Install:

- Assumes you have both [upstream HPI](https://github.com/karlicoss/HPI) and [my HPI](https://github.com/seanbreckenridge/HPI) modules installed
- Setup [upstream `promnesia`](https://github.com/karlicoss/promnesia)
- Install this; `python3 -m pip install git+https://github.com/seanbreckenridge/promnesia`

If you have issues importing/installing this, try a local install isntead. See [troubleshooting docs](https://github.com/seanbreckenridge/HPI/blob/master/doc/TROUBLESHOOTING_INSTALLS.md)

In your config file, to enable these sources, import from `promnesia_sean`. You can see my [config file](https://sean.fish/d/promnesia/config.py?dark) as an example
