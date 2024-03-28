import xarm
import json
import os

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
        new_position = max(-125.0, min(125.0, new_position))

        # Update the servo state and move the servo
        self.update_servo_state(servo_id, new_position)
        self.arm.setPosition([[servo_id, new_position]], wait=True)


    # Additional methods for advanced control and integration with other modules

    def define_macros(self):
        self.macros = {
            "default": [[1, 0.0], [2, 0.0], [3, 0.0], [4, 0.0], [5, 0.0], [6, 0.0]],

            "hook-to-x": [ [2, 0.0], [3, 90.0], [4, 0.0], [5, 0.0], [6, 90.0]],
            "hook-down-x":[ [2, 0.0], [3, 90.0], [4, -70.0], [5, 0.0], [6, 90.0]],
            "reach-out-x":[ [2, 0.0], [3, 30.0], [4, -70.0], [5, 20.0], [6, 90.0]],

            "hook-to-y": [ [2, 0.0], [3, 90.0], [4, 0.0], [5, 0.0], [6, 0.0]],
            "hook-down-y":[ [2, 0.0], [3, 90.0], [4, -70.0], [5, 0.0], [6, 0.0]],
            "reach-out-y":[ [2, 0.0], [3, 30.0], [4, -70.0], [5, 20.0], [6, 0.0]],

            "open": [[1, -90.0]],
            "close": [[1, 90.0]]
        }

    def execute_macro(self, name):
        if name in self.macros:
            macro = self.macros[name]
            movements = []  # This will store all movements
            
            # Handle macros defined as sequences of dictionaries
            # (for complex, sequential movements)
            if all(isinstance(movement, dict) for movement in macro):  
                for movement in macro:
                    for servo_id, position in movement.items():
                        movements.append([servo_id, position])
                self.arm.setPosition(movements, wait=True)
            
            else: # Handle macros defined as list of lists for parallel movement
                for movement in macro:
                    if isinstance(movement, list) and len(movement) == 2:
                        # Add the movement directly to the movements list
                        movements.append(movement)

                if movements:  # Check if there are any movements to execute
                    self.arm.setPosition(movements, wait=True)

    def save_macro_sequence(self, sequence_name, macro_names):
        """Saves a sequence of macros to a file within the specified directory."""
        sequences_dir = os.path.join(os.path.dirname(__file__), "macro_sequences")
        os.makedirs(sequences_dir, exist_ok=True)
        
        file_path = os.path.join(sequences_dir, f"{sequence_name}.json")
        with open(file_path, 'w') as file:
            json.dump(macro_names, file)

    def load_macro_sequence(self, sequence_name):
        """Loads a macro sequence from a file within the specified directory."""
        file_path = os.path.join(os.path.dirname(__file__), "macro_sequences", f"{sequence_name}.json")
        try:
            with open(file_path, 'r') as file:
                macro_names = json.load(file)
            return macro_names
        except FileNotFoundError:
            print(f"Sequence '{sequence_name}' not found.")
            return []
        
    def execute_macro_sequence(self, sequence_name):
        """Executes a saved sequence of macros."""
        macro_names = self.load_macro_sequence(sequence_name)
        for name in macro_names:
            self.execute_macro(name)
            # Consider adding a short delay here if needed between macro executions

'''
    def execute_macro(self, name):
        if name in self.macros:
            macro = self.macros[name]
            if all(isinstance(movement, dict) for movement in macro):  # Check if all elements are dictionaries
                for movement in macro:
                    # Execute each movement in the sequence
                    for servo_id, position in movement.items():
                        self.update_servo_state(servo_id, position)
                        # Since the setPosition expects a list of [servo_id, position], wrap it in a list
                        self.arm.setPosition([[servo_id, position]], wait=True)
            else:  # Handle single movements or non-sequential macros
                for movement in macro:
                    if isinstance(movement, list) and len(movement) == 2:
                        servo_id, position = movement
                        self.update_servo_state(servo_id, position)
                        self.arm.setPosition([movement], wait=True)
'''

        