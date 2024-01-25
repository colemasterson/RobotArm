# controllers/servo_controller.py
import xarm

class ServoController:
    def __init__(self, servo_id, arm):
        self.servo_id = servo_id  # Store the servo ID
        self.servo = xarm.Servo(servo_id)
        self.arm = arm

    def get_position(self):
        return self.arm.getPosition(self.servo, True)

    def set_position(self, position, wait=False):
        self.arm.setPosition([[self.servo_id, position]], wait=wait)  # Use stored servo ID
