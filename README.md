## promnesia

This lets me use [my own HPI modules](https://github.com/seanbreckenridge/HPI) as additional `Source`s for [promnesia](https://github.com/karlicoss/promnesia).

It indexes any URLs it finds in my:

- Discord messages, [parsed from the data export](https://github.com/seanbreckenridge/discord_data)
- Browser history from my [ffexport](https://github.com/seanbreckenridge/ffexport) (firefox) backups
- Podcasts/Videos I watched with mpv (tracked by [this](https://github.com/seanbreckenridge/mpv-history-daemon))
- comments from some [old forums](https://github.com/seanbreckenridge/forum_parser) I used to be on
- Youtube videos/comments [parsed](https://github.com/seanbreckenridge/HPI/tree/master/my/google) from my [google takeout](https://takeout.google.com/)
- Movies/TV Show episodes tracked by my [trakt](https://github.com/seanbreckenridge/traktexport)
- Shell histories (zsh, [ttt](https://github.com/seanbreckenridge/ttt), ipython)
- SMS history, using [SMSBackupRestore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en_US)
- Git commits on my system
- Github PRs/Issues/Comments, using [ghexport](https://github.com/karlicoss/ghexport)
- Todo.txt files
- Albums [I've listened to](https://sean.fish/s/albums)
- Facebook Messages

[My Promnesia config file](https://sean.fish/d/promnesia/config.py)

### Install

For the time being, this doesn't install as a namespace package alongside `promnesia`, it just installs a separate module, `promnesia_sean`. See the comments [here](https://github.com/karlicoss/promnesia/pull/225) for more info.

To Install:

- Assumes you have both [upstream HPI](https://github.com/karlicoss/HPI) and [my HPI](https://github.com/seanbreckenridge/HPI) modules installed
- Setup the [upstream `promnesia`](https://github.com/karlicoss/promnesia)
- `python3 -m pip install 'git+https://github.com/seanbreckenridge/promnesia`

In your config file, to enable these sources, import from `promnesia_sean`. You can see my [config file](https://sean.fish/d/promnesia/config.py) as an example
