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
        speed = 360
        self.motor_left.run_timed(time_sp=time, speed_sp=speed)
        self.motor_right.run_timed(time_sp=time, speed_sp=speed)
        self.motor_left.wait_while('running')
        self.motor_right.wait_while('running')

    def forward(self, time, speed):
        self.motor_left.run_timed(time_sp=time, speed_sp=speed)
        self.motor_right.run_timed(time_sp=time, speed_sp=speed)
        self.motor_left.wait_while('running')
        self.motor_right.wait_while('running')

    # stops all motors
    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

    # unlock wheels
    def free_motor(self):
        self.motor_left.stop(stop_action='coast')
        self.motor_right.stop(stop_action='coast')

    # lock wheels, set to brake
    def brake_motor(self):
        self.motor_left.stop(stop_action='brake')
        self.motor_right.stop(stop_action='brake')

    # resets measured position of the wheels to 0
    def reset_position(self):
        self.motor_left.position = 0
        self.motor_right.position = 0

    # returns the measured position of the wheels
    def get_position(self):
        position = (self.motor_left.position, self.motor_right.position)
        return position

    # drive with separate speeds for left and right wheel to allow turns
    # 3 parameters -> time: in ms, speed_left: speed for left wheel, speed_right: speed for right wheel
    def move_left_right(self, time, speed_left, speed_right):
        self.motor_left.run_timed(time_sp=time, speed_sp=speed_left)
        self.motor_right.run_timed(time_sp=time, speed_sp=speed_right)

        #self.motor_left.wait_while('running')
        #self.motor_right.wait_while('running')

    # runs the motors without timed runtime
    def move_lr_steady(self, speed_left, speed_right):
        self.motor_left.run_forever(speed_sp = speed_left)
        self.motor_right.run_forever(speed_sp = speed_right)

    def wait(self):
        self.motor_left.wait_while('running')
        self.motor_right.wait_while('running')