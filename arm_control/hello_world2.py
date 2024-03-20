from arm_controller import RobotArmController
import time

def test_robot_arm():
    # Initialize the Robot Arm Controller
    arm_controller = RobotArmController()

    # Define the macros
    arm_controller.define_macros()

    """
    # Test some macros
    print("Executing 'default' macro...")
    arm_controller.execute_macro("default")
    time.sleep(2)
    """
   # arm_controller.arm.setPosition([[1, 0.0], [2, 0.0], [3, -90.0], [4, 0.0], [5, 0.0], [6, 0.0]], wait = True)

    print("Executing 'Rotate_Claw' macro...")
   # arm_controller.execute_macro("rotate_claw")
    time.sleep(2)
  
    print("Executing 'open' macro...")
    arm_controller.execute_macro("open")
    time.sleep(2)

    print("Executing 'close' macro...")
    arm_controller.execute_macro("close")
    time.sleep(2)

if __name__ == "__main__":
    test_robot_arm()
