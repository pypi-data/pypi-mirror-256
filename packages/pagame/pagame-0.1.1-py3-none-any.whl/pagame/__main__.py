from .game import Game


LANGUAGE = "en"
PLAYLIST = "6TutgaHFfkThmrrobwA2y9"


def main():
    """Start the game."""
    print("Enter the delay (in minutes) between each round.")
    minimum = maximum = None
    while not (minimum and maximum):
        try:
            minimum = float(input(" > Minimum: "))
            maximum = float(input(" > Maximum: "))
        except ValueError:
            print("   ! Invalid input. Please try again. !")

    language = input("Enter the language to use (e.g., EN or NO): ").lower()

    playlist = input("Enter the main Spotify playlist uri: ")
    spotify_id = input("Enter the Spotify client id: ")
    spotify_secret = input("Enter the Spotify client secret: ")

    Game(
        delay=(minimum, maximum),
        language=LANGUAGE if not language else language,
        music={
         "playlist": "spotify:playlist:" + PLAYLIST if not playlist else playlist,
         "directory": "./lookup/sounds/",
         "spotify": {
             "client_id": spotify_id,
             "client_secret": spotify_secret,
             "redirect_uri": "http://localhost:3000/callback"
         }
        }
    )


if __name__ == "__main__":
    main()
