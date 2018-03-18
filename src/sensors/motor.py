import ev3dev.ev3 as ev3


class Motor:

    # constructor: setup corresponding EV3 outputs
    def __init__(self):
        self.motor_left = ev3.LargeMotor('outA')
        self.motor_right = ev3.LargeMotor('outD')
        # slow preset speed
        self.speed = 100

    # driving forward for a specific time
    # 1 parameter -> time: how long to drive in ms
    def forward(self, time):
        self.motor_left.run_timed(time_sp=time, speed_sp=self.speed)
        self.motor_right.run_timed(time_sp=time, speed_sp=self.speed)

    # drive with separate speeds for left and right wheel to allow turns
    # 3 parameters -> time: in ms, speed_left: speed for left wheel, speed_right: speed for right wheel
    def move_left_right(self, time, speed_left, speed_right):
        self.motor_left.run_timed(time_sp=time, speed_sp=speed_left)
        self.motor_right.run_timed(time_sp=time, speed_sp=speed_right)
