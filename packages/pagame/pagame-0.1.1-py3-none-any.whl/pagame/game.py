from .contestants import Contestants, BUTTON_SIZE
from .sound import Noise, VOLUME

import time
import random
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QListWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QGroupBox)


class Game(QMainWindow):
    """The game class controlling everything."""
    def __init__(self, delay, language, music):
        self.app = QApplication([])
        self.app.setStyleSheet("""
            QPushButton {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
            }
            QPushButton:hover {
                background-color: #ECEBE5;
            }
            QPushButton:pressed {
                background-color: #D6D5D1;
            }
            QGroupBox {
                border: 1px solid gray;
                border-radius: 4px;
                margin-top: 0.5em;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                color: gray;
            }
            QListWidget {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
            }
            QListWidget::item:selected {
                background-color: #FBFAF5;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #ECEBE5;
            }
            QLineEdit {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
            }
            QComboBox {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
            }
        """)
        super().__init__()

        self.volume = VOLUME
        self.Sound = Noise(language=language, **music)
        self.Contestants = Contestants()

        self.modes = {
            getattr(self, mode).__name__.replace("_", " ").capitalize(): getattr(self, mode)
            for mode in set(dir(self)) - set(dir(QMainWindow))
            if not mode.startswith("_") and callable(getattr(self, mode))
        }
        custom = {k: v for k, v in self.modes.items() if k.endswith("x")}
        self.modes = {k: v for k, v in sorted(self.modes.items(), key=lambda x: x[0])
                      if k not in custom}
        custom = {f"({(k.replace(' x', ''))})": v for k, v in custom.items()}
        self.modes.update(custom)

        self.delay = tuple(int(i * 60000)
                           for i in (delay if isinstance(delay, tuple) else (delay, delay)))
        self.delay = (min(self.delay), max(self.delay))

        self._continue = None
        self._timer = None

        self._textfiles()
        self._graphics()

        self.show()
        self.setWindowIcon(QIcon("./lookup/icons/icon.png"))
        self.app.exec_()

    def _textfiles(self):
        """Reads the textfiles."""
        self.categories = []
        with open("./lookup/textfiles/categories.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                self.categories.append(line)

        self.most_likely_to = []
        with open("./lookup/textfiles/likely_to.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                self.most_likely_to.append(line)

        self.lyrics = []
        with open("./lookup/textfiles/lyrics.txt", "r", encoding="utf-8") as file:
            for line in file:
                info, text = line.split(" [] ")
                artist, song = info.split(", ")
                self.lyrics.append((artist, song, text))

    def _graphics(self):
        """Creates the GUI."""
        self.setGeometry(0, 0, 100, 200)

        central = QWidget()
        self.setCentralWidget(central)
        self.setWindowTitle("P4R7Y T13M!")

        self.layout = QVBoxLayout()
        central.setLayout(self.layout)

        self._graphics_top()
        self._graphics_bottom()

    def _graphics_top(self):
        """Creates the top part of the GUI."""
        top = QHBoxLayout()

        left = QGroupBox("Controls")
        controls = QVBoxLayout()
        playback = QHBoxLayout()
        feedback = QHBoxLayout()

        pause = QPushButton()
        pause.setIcon(QIcon("./lookup/icons/pause.png"))
        pause.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        pause.clicked.connect(self.Sound.pause_music)  # noqa
        playback.addWidget(pause)

        play = QPushButton()
        play.setIcon(QIcon("./lookup/icons/play.png"))
        play.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        play.clicked.connect(self.Sound.unpause_music)  # noqa
        playback.addWidget(play)

        skip = QPushButton()
        skip.setIcon(QIcon("./lookup/icons/skip.png"))
        skip.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        skip.clicked.connect(self.Sound.skip_music)  # noqa
        playback.addWidget(skip)

        down = QPushButton()
        down.setIcon(QIcon("./lookup/icons/volume-down.png"))
        down.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        down.clicked.connect(self._decrease_volume)  # noqa
        feedback.addWidget(down)

        up = QPushButton()
        up.setIcon(QIcon("./lookup/icons/volume-up.png"))
        up.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        up.clicked.connect(self._increase_volume)  # noqa
        feedback.addWidget(up)

        self.button_start = QPushButton("START")
        self.button_start.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_start.clicked.connect(self._start_game)  # noqa
        feedback.addWidget(self.button_start)

        self.button_continue = QPushButton()
        self.button_continue.setIcon(QIcon("./lookup/icons/continue.png"))
        self.button_continue.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_continue.clicked.connect(self._pass)  # noqa
        self.button_continue.hide()
        feedback.addWidget(self.button_continue)

        self.button_disable = QPushButton()
        self.button_disable.setIcon(QIcon("./lookup/icons/power.png"))
        self.button_disable.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_disable.clicked.connect(self._disable)  # noqa
        self.button_disable.hide()
        feedback.addWidget(self.button_disable)

        playback.setSpacing(20)
        feedback.setSpacing(20)
        controls.addLayout(playback)
        controls.addLayout(feedback)

        left.setLayout(controls)
        left.setObjectName("left")
        left.setStyleSheet("""
            QWidget#left {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)
        top.addWidget(left)

        right = QGroupBox("Contestants")
        inside = QVBoxLayout()
        inside.addWidget(self.Contestants)
        right.setLayout(inside)
        right.setFixedWidth(BUTTON_SIZE * 5)
        right.setObjectName("right")
        right.setStyleSheet("""
            QWidget#right {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)
        top.addWidget(right)

        self.layout.addLayout(top)

    def _graphics_bottom(self):
        """Creates the bottom part of the GUI."""
        bottom = QHBoxLayout()

        left = QGroupBox("Add game")
        addition = QVBoxLayout()

        adding = QComboBox()
        adding.addItems(self.modes.keys())
        adding.setFixedHeight(BUTTON_SIZE // 2)
        adding.setStyleSheet("""
            QComboBox::drop-down {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
                color: gray;
            }
            QComboBox::drop-down:hover {
                background-color: #ECEBE5;
            }
            QComboBox::item:selected {
                background-color: #ECEBE5;
                color: black;
            }
            QComboBox::item {
                background-color: #FBFAF5;
                color: gray;
            }
        """)

        add = QPushButton()
        add.setIcon(QIcon("./lookup/icons/add.png"))
        add.clicked.connect(lambda: self._add_mode(adding.currentText()))  # noqa
        add.setFixedHeight(BUTTON_SIZE)

        addition.addWidget(adding)
        addition.addWidget(add)

        left.setLayout(addition)
        left.setObjectName("left")
        left.setStyleSheet("""
            QWidget#left {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)
        left.setFixedWidth(int(BUTTON_SIZE * 3.5))
        bottom.addWidget(left)

        right = QGroupBox("Active games")
        activated = QVBoxLayout()

        self.activated = QListWidget()
        self.activated.itemClicked.connect(self._remove_mode)  # noqa
        for mode in self.modes:
            self.activated.addItem(mode) if not mode.startswith("(") else None
        self.activated.sortItems()
        activated.addWidget(self.activated)

        right.setLayout(activated)
        bottom.addWidget(right)

        self.layout.addLayout(bottom)

    def _increase_volume(self):
        """Increases the volume."""
        self.volume = min(self.volume + 5, 100)
        try:
            self.Sound.music.volume(self.volume)
        except AttributeError:
            pass

    def _decrease_volume(self):
        """Decreases the volume."""
        self.volume = max(self.volume - 5, 0)
        try:
            self.Sound.music.volume(self.volume)
        except AttributeError:
            pass

    def _add_mode(self, mode):
        """Adds a game mode."""
        self.activated.addItem(mode)
        self.activated.sortItems()

    def _remove_mode(self, mode):
        """Renmoves a game mode."""
        self.activated.takeItem(self.activated.row(mode))

    def _start_game(self):
        """Starts the game."""
        if len(self.Contestants.contestants) < 2:
            self.Sound.read("Dude... You can't seriously be trying to play this alone.")

            if self.Sound.music:
                self.Sound.music.volume(100)
                self.Sound.music.start_playback(uris=["spotify:track:0nr2FxkTgIwCjDdUC50gPI"])
                self.Sound.music.repeat("track")

            return

        self.button_start.hide()
        self.button_disable.show()

        self.Sound.pause_music()

        self.Sound.read(f"Welcome to the drinking {', '.join(self.Contestants.contestants)}",
                        override=True)
        self.Sound.read("Let the games begin!")

        self.Sound.unpause_music()

        self.timer = QTimer()
        self.timer.timeout.connect(self._game_loop)  # noqa
        self.timer.start(1000)

    def _game_loop(self):
        """The game loop."""
        try:
            index = random.randint(0, self.activated.count() - 1)
            self.modes[self.activated.item(index).text()]()
        except ValueError:
            pass

        wait = random.randint(self.delay[0], self.delay[1])
        self.timer.start(wait)

    def _pass(self):
        """Continues the game."""
        self._continue = True
        self.button_continue.hide()
        self.button_disable.show()

    def _disable(self):
        """Disables the game."""
        self.timer.stop()
        self._continue = False
        self.button_disable.hide()
        self.button_continue.show()

        def continues():
            if not self._continue:
                return

            self.timer.start(1000)
            self._timer.stop()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)  # noqa
        self._timer.start(12000)

    def drink_bitch(self):
        """Drink bitch game mode."""
        the_bitch = random.choice(self.Contestants.contestants)

        self.Sound.pause_music()

        self.Sound.read(f"Could I get your attention, please?")

        time.sleep(2)

        self.Sound.read(f"{the_bitch} drink. Bitch.")

        self.Sound.unpause_music()

    def music_quiz(self):
        """Music quiz game mode."""
        self.Sound.pause_music()

        self.Sound.read("Welcome to the music quiz.")
        self.Sound.read("I am going to play three songs for you.")
        self.Sound.read("The first person to shout out the name of the song or the artist wins")
        self.Sound.read("and may hand out one to two sips.")

        # Sometimes the ID doesn't match the artist and name:

        songs = self.Sound.music.playlist_tracks("2sbw07iogIXbWpmOz0U66W")["items"]
        random.shuffle(songs)

        for i in range(1, 4):
            if i != 3:
                self.Sound.read(f"Song number {i}")
            else:
                self.Sound.read("Last song")

            song = songs[i]["track"]
            song_id = song["id"]
            song_name = song["name"]
            artist_name = song["artists"][0]["name"]

            self.Sound.music.add_to_queue(song_id)
            self.Sound.skip_music()

            time.sleep(25)

            self.Sound.pause_music()

            time.sleep(1)

            self.Sound.read(f"{song_name} by, {artist_name}", override=True)

        action = random.choice(["handing out 1 sip",
                                "handing out 2 sips",
                                "handing out 3 sips",
                                "drinking 1 sip",
                                "drinking 2 sips",
                                "drinking 3 sips",
                                "the fact that you are great in bed",
                                "the fact that you are a great person",
                                "the fact that you are a great friend"])
        self.Sound.read(f"If you got all correct, you can comfort yourself by {action}.")

        self.Sound.skip_music()

    def categories(self):
        """Category game mode."""
        self.Sound.pause_music()

        category = random.choice(self.categories)
        starting = random.choice(self.Contestants.contestants)

        self.Sound.read("This is the category game.")
        self.Sound.read("Say something within the category until someone fails.")
        self.Sound.read("Click to continue.")

        self.Sound.read("The category is:")
        self.Sound.read(f"{category}, and {starting} is starting.")

        self._continue = False
        self.button_disable.hide()
        self.button_continue.show()

        def continues():
            if not self._continue:
                return

            self._timer.stop()

            time.sleep(1)

            action = random.choice(["drink 3 sips.",
                                    "drink 2 sips.",
                                    "drink 1 sip.",
                                    "give out 3 sips.",
                                    "give out 2 sips.",
                                    "give out 1 sip."])
            self.Sound.read(f"The loser has to {action}.")

            time.sleep(1)
            self.Sound.unpause_music()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)  # noqa
        self._timer.start(1000)

    def most_likely(self):
        """Most likely to game mode."""
        self.Sound.pause_music()
        self.Sound.read("Shut up! This is the most likely game.")
        self.Sound.read("I will read a statement plus name, and you will decide if it is true.")
        self.Sound.read("If the majority says it is true, the person has to drink.")
        self.Sound.read("If the majority says it is false, the person can give out 3 sips.")

        for i in range(3):
            person = random.choice(self.Contestants.contestants)
            action = random.choice(self.most_likely_to)

            self.Sound.read(f"{person} is the most likely to {action}")

            time.sleep(10)

        self.Sound.unpause_music()

    def waterfall(self):
        """Waterfall game mode."""
        self.Sound.pause_music()

        self.Sound.read("Shut your mouth and pay attention. The next game is waterfall.")

        person = random.choice(self.Contestants.contestants)
        self.Sound.read(f"{person} starts and decides the direction.")

        time.sleep(2)

        self.Sound.unpause_music()

    def lyrical_master(self):
        """Lyricsmaster game mode."""
        self.Sound.pause_music()
        self.Sound.read("Welcome to the lyrical master.")
        self.Sound.read("I will read some lyrics and you must guess the song.")

        artist, song, text = random.choice(self.lyrics)

        self.Sound.read(text.strip(), override=True)

        time.sleep(5)

        self.Sound.read(f"The song was {song} by {artist}")

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip."])
        self.Sound.read(f"The winner has to {action}.")

        self.Sound.unpause_music()

    def last_to(self):
        """Last person to game."""
        self.Sound.pause_music()

        self.Sound.read("Last person who")
        activity = random.choice(["Dabs",
                                  "Drinks",
                                  "Takes a shot",
                                  "Stands up",
                                  "Lays down"])
        self.Sound.read(f"{activity}")

        time.sleep(2)

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip."])
        self.Sound.read(f"May {action}.")

        self.Sound.unpause_music()

    def grimace(self):
        """Best grimace game."""
        self.Sound.pause_music()

        self.Sound.read("Everyone make a grimace!")

        time.sleep(2)

        self.Sound.read("Point at the person with the best grimace.")

        time.sleep(8)

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip."])
        self.Sound.read(f"The winner must {action}")

        time.sleep(1)

        self.Sound.unpause_music()

    def build(self):
        """Building game."""
        self.Sound.pause_music()

        self.Sound.read("The person to build the highest tower of HIS OWN empty cans wins.")

        delay = random.choice([2, 5, 10, 12, 15, 17])

        self.Sound.read(f"You have {delay} seconds.")

        time.sleep(delay)

        self.Sound.read("Stop!")

        time.sleep(2)

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip.",
                                "give out the amount of cans in your tower.",
                                "sip the amount of cans in your tower."])
        self.Sound.read(f"The winner must {action}")

        time.sleep(2)

        self.Sound.unpause_music()

    def snacks(self):
        """Throw snacks!"""
        self.Sound.pause_music()

        self.Sound.read("One person at a time must try and throw snacks into their mouth.")
        self.Sound.read("The first person to manage it wins.")
        self.Sound.read(f"{random.choice(self.Contestants.contestants)} starts.")
        self.Sound.read("Click to continue")

        self._continue = False
        self.button_disable.hide()
        self.button_continue.show()

        def continues():
            if not self._continue:
                return

            self._timer.stop()

            action = random.choice(["drink 3 sips.",
                                    "drink 2 sips.",
                                    "drink 1 sip.",
                                    "give out 3 sips.",
                                    "give out 2 sips.",
                                    "give out 1 sip.",
                                    "give out as many sips as tries it took.",
                                    "drink as many sips as tries it took."])
            self.Sound.read(f"The winner must {action}")

            time.sleep(5)

            self.Sound.unpause_music()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)  # noqa
        self._timer.start(1000)

    def mime(self):
        """Mime game."""
        self.Sound.pause_music()

        self.Sound.read("Miming game! Think of what you are going to mime!")

        time.sleep(5)

        delay = random.choice([5, 10, 12, 15, 17, 20])
        self.Sound.read(f"{random.choice(self.Contestants.contestants)} "
                        f"is miming and has {delay} seconds.")

        time.sleep(delay)

        self.Sound.read("Stop!")
        self.Sound.read("Those who could not guess has to drink.")
        self.Sound.read("If no one managed, the mime must drink.")

        time.sleep(2)

        self.Sound.unpause_music()

    def thumb_war(self):
        """Thumb war game."""
        try:
            person_1, person_2 = random.sample(self.Contestants.contestants, 2)
            self.Sound.pause_music()
        except ValueError:
            return

        self.Sound.read(f"Thumb war between {person_1} and {person_2}!")

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip.",
                                "give out as many sips as tries it took.",
                                "drink as many sips as tries it took."])
        person = random.choice(["winner", "loser"])
        self.Sound.read(f"The {person} must {action}")

        time.sleep(20)

        self.Sound.unpause_music()

    def slap_the_mini(self):
        """Mini game."""
        self.Sound.pause_music()

        self.Sound.read("Slap the closest mini!")

        time.sleep(2)

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip.",
                                "give out as many sips as slaps.",
                                "drink as many sips as slaps."])
        self.Sound.read(f"The slapped minis must {action}")

        self.Sound.unpause_music()

    def karin_henter_x(self):
        """Karin er tjener!"""
        self.Sound.pause_music()

        self.Sound.read("Beer-round!")
        self.Sound.read("Karin fetches drinks to everyone that wants!")
        time.sleep(10)

        self.Lyd.unpause_music()

    def andreas_round_x(self):
        """Andreas game."""
        self.Sound.pause_music()

        self.Sound.read("Andreas' round!")
        time.sleep(2)
        self.Sound.read("Which song is this?")
        time.sleep(1)

        self.Sound.unpause_music()
