# controllers/macro_controller.py

import xarm
from .servo_controller import ServoController

class RobotArmController:
    def __init__(self):
        self.arm = xarm.Controller('USB')
        print('Battery voltage in volts:', self.arm.getBatteryVoltage())
        self.servo_states = {1: {'position': None, 'speed': None},
                             2: {'position': None, 'speed': None},
                             3: {'position': None, 'speed': None},
                             4: {'position': None, 'speed': None},
                             5: {'position': None, 'speed': None},
                             6: {'position': None, 'speed': None},}
        self.servo_controllers = {}
        for servo_id in range(1, 6):
            self.servo_controllers[servo_id] = ServoController(servo_id, self.arm)

        self.init_servo_states()

    def init_servo_states(self):
        for servo_id, servo_controller in self.servo_controllers.items():
            position = servo_controller.get_position()
            self.servo_states[servo_id] = {'position': position, 'speed': None}
    
    def update_servo_state(self, servo_id, position, speed=None):
        self.servo_states[servo_id]['position'] = position
        self.servo_states[servo_id]['speed'] = speed

        # function for adjusting the angle for a specific servo, used in the new GUI.
    
        # servo_id (int): The ID of the servo to be adjusted.
        # delta (float): The amount to change the angle, can be positive or negative.
        
    def adjust_servo_angle(self, servo_id, delta):
        if servo_id not in self.servo_controllers:
            print(f"Invalid servo ID: {servo_id}")
            return

        servo_controller = self.servo_controllers[servo_id]
        current_position = servo_controller.get_position()
        if current_position is None:
            print(f"Servo {servo_id} position is not initialized.")
            return

        new_position = max(-125.0, min(125.0, current_position + delta))
        servo_controller.set_position(new_position, wait=True)
        self.update_servo_state(servo_id, new_position)


    # Additional methods for advanced control and integration with other modules

    def define_macros(self):
        self.macros = {
            "default": [[1, 0.0], [2, 0.0], [3, 0.0], [4, 0.0], [5, 0.0], [6, 0.0]],
            "south_down": [[1, 0.0], [2, 0.0], [3, 0.0], [4, -75.0], [5, 10.0], [6, 0.0]],
            "south_west": [[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]],
            "south_east": [[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]],

            "rotate_claw": [
                {2: 90.0},
                {2: -90.0},
                {2: 0.0}
            ],

            "open": [[1, -90.0]],
            "close": [[1, 90.0]]
        }
    
    def get_servo_state(self, id,):
        return self.servo_controllers(id)

    def execute_macro(self, name):
        if name in self.macros:
            for movement in self.macros[name]:
                # Merge the current servo states with the movement
                merged_positions = []
                for servo_id in range(1, 6):
                    if servo_id in movement:
                        position = movement[servo_id]
                    else:
                        position = self.get_servo_state(servo_id)['position']
                    merged_positions.append([servo_id, position])

                self.arm.setPosition(merged_positions, wait = True)
