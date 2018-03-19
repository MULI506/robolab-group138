import ev3dev.ev3 as ev3


class Sounds:

    def __init__(self):
        self.sounds = ev3.Sound

    def say_red(self):
        self.sounds.speak("red red").wait()

    def say_blue(self):
        self.sounds.speak("blue blue").wait()

