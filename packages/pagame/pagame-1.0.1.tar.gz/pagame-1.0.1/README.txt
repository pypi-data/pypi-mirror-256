Have fun.

Install using `pip install pagame`.

Run from terminal: `pagame`

Run from python:

```python
    from pagame import play

    play()
```

See and run `examples/example_game.py` for manually starting the game.

Notes
-----
    Spotify should be open for the proper experience, but does not have to.

    In order for the game to access Spotify, you need to have a Spotify client id and secret. These
    can be obtained by creating a Spotify app (through 'developer.spotify.com'); and the client id
    and secret can be pasted directly in the script entered in terminal when runni

    When this is in order, run the `play.py`-script from the root directory.

Parameters
----------
    DELAY           : Minutes between each game.
                      `int` or `tuple`
                        If a tuple, the game will start at a random time between the two values.

    LANGUAGE        : Language to play the game in.
                      `str`
                        Example: "en" for English, "no" for Norwegian.

    PLAYLIST        : Spotify-URI for the playlist.
                      `str`

    SPOTIFY_ID      : Spotify client id.
                      `str`
    SPOTIFY_SECRET  : Spotify client secret.
                      `str`
