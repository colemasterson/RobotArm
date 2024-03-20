import xarm

class RobotArmController:
    def __init__(self):
        # Initialize connection with the robot arm and update initial states
        self.arm = xarm.Controller('USB')
        print('Battery voltage in volts:', self.arm.getBatteryVoltage())

        self.servo_states = {1: {'position': None, 'speed': None},
                             2: {'position': None, 'speed': None},
                             3: {'position': None, 'speed': None},
                             4: {'position': None, 'speed': None},
                             5: {'position': None, 'speed': None},
                             6: {'position': None, 'speed': None},}

       # Now, we can initialize the position values 
        self.init_servo_states()

    def get_servo_state(self, servo_id):
        # Check if the servo ID is valid and exists in the servo_states dictionary
        if servo_id in self.servo_states:
            return self.servo_states[servo_id]
        else:
            print(f"Servo ID {servo_id} is not valid or not initialized.")
            return None

    def init_servo_states(self):
        # Populate the servo_states dictionary with initial positions
        for servo_id in self.servo_states:
            servo = xarm.Servo(servo_id)
            position = self.arm.getPosition(servo, True)
            self.servo_states[servo_id]['position'] = position
    
    def update_servo_state(self, servo_id, position, speed=None):
        # Update the state of a single servo
        self.servo_states[servo_id]['position'] = position
        self.servo_states[servo_id]['speed'] = speed
        # Send command to the hardware to move the servo
        #self.arm.setPosition([int(servo_id), float(position)], wait = True)
    # function for adjusting the angle for a specific servo, used in the new GUI.
  
    # servo_id (int): The ID of the servo to be adjusted.
    # delta (float): The amount to change the angle, can be positive or negative.
    
    def adjust_servo_angle(self, servo_id, delta):
        # Ensure the servo_id is valid
        if servo_id not in self.servo_states:
            print(f"Invalid servo ID: {servo_id}")
            return

        # Calculate the new position
        current_position = self.servo_states[servo_id]['position']
        if current_position is None:
            print(f"Servo {servo_id} position is not initialized.")
            return

        new_position = current_position + delta

        # Bound the new position within the range [-90, 90]
        new_position = max(-90, min(90, new_position))

        # Update the servo state and move the servo
        self.update_servo_state(servo_id, new_position)
        self.arm.setPosition([[servo_id, new_position]], wait=True)


    # Additional methods for advanced control and integration with other modules

    def define_macros(self):
        self.macros = {
            "default": [[1, 0.0], [2, 0.0], [3, 0.0], [4, 0.0], [5, 0.0], [6, 0.0]],
            "south_down": [[1, 0.0], [2, 0.0], [3, 0.0], [4, -75.0], [5, 10.0], [6, 0.0]],
            "south_west": [[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]],
            "south_east": [[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]],

            # This one might be tricky to get running, we'll see if it works the way it is
            "rotate_claw": [
                {2: 90.0},
                {2: -90.0},
                {2: 0.0}
            ],

            "open": [[1, 90.0]],
            "close": [[1, 0.0]]
        }

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
        