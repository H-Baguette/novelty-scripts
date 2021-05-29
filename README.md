# Novelty Scripts
A collection of bad, pointless scripts that I make when I get bored.

- [SA Probetime Badge](#sa-probetime-badge)

### SA Probetime Badge
A forum signature badge that keeps track of how long youve been probed for on the SomethingAwful forums. Currently only tracks the 50 most recent probations, because web scraping is a pain in the ass. Working on it, though! Feel free to make a PR if you want to fix it yourself.
![My Probetime Badge](http://baguette.sdf.org/badges/scripts/probebadge.png "My Probetime Badge")

#### Setup
- Copy the `probebadge` folder somewhere on your webserver - somewhere publicly accessible.
- Change the value of  `horribleJerk` in `probebadge.py` to the UserID of the poster you want in your badge.
- Set up a cron job to automatically run `probebadge.py` at whatever interval you want. Be reasonable, though.
- Copy the web link to `probebadge.png` to your forum signature, or wherever you want to display the badge.