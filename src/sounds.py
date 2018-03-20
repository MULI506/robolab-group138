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

    def say_obstacle(self):
        self.sounds.speak("rrrr").wait()

    def say_down(self):
        self.sounds.tone([(550, 150, 50), (500, 150, 50), (450, 150, 50), (400, 150, 50),
                          (350, 150, 50), (300, 150, 50), (250, 150, 50), (200, 150, 50),
                          (150, 150, 50), (100, 150, 50), (90, 150, 50), (80, 150, 50)]).wait()

    def say_coordinate(self, position, direction):
        position_x = position[0]
        position_y = position[1]
        self.sounds.speak("new position ").wait()
        self.sounds.speak(position_x).wait()
        self.sounds.speak("and").wait()
        self.sounds.speak(position_y).wait()
        self.sounds.speak("direction is").wait()
        self.sounds.speak(direction).wait()