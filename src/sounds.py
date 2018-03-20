import ev3dev.ev3 as ev3


class Sounds:

    def __init__(self):
        self.sounds = ev3.Sound

    def say_red(self):
        self.sounds.speak("red").wait()

    def say_blue(self):
        self.sounds.speak("blue").wait()

    def say_white(self):
        self.sounds.speak("white").wait()

    def say_black(self):
        self.sounds.speak("black").wait()

    def say_oooo(self):
        self.sounds.speak("oooo").wait()

