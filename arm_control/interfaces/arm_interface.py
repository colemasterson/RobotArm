import xarm;

# interfaces/arm_interface.py

from ..controllers.servo_controller import ServoController

class ArmInterface:
    def __init__(self, connection_type='USB'):
        self.arm = xarm.Controller(connection_type)
        self.servos = [ServoController(i, self.arm) for i in range(1, 7)]

    def get_servo_position(self, servo_id):
        return self.servos[servo_id - 1].get_position()

    def set_servo_position(self, servo_id, position, wait=False):
        self.servos[servo_id - 1].set_position(position, wait)

