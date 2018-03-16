import ev3dev.ev3 as ev3


class Motor:

    def __init__(self):
        self.motor_left = ev3.LargeMotor('outA')
        self.motor_right = ev3.LargeMotor('outD')
        self.speed = 100

    def forward(self, time):
        self.motor_left.run_timed(time_sp=time, speed_sp=self.speed)
        self.motor_right.run_timed(time_sp=time, speed_sp=self.speed)

    def move_left_right(self, time, speed_left, speed_right):
        self.motor_left.run_timed(time_sp=time, speed_sp=speed_left)
        self.motor_right.run_timed(time_sp=time, speed_sp=speed_right)