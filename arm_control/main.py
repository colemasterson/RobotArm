from interfaces.arm_interface import ArmInterface
import xarm;

def main():
    arm = ArmInterface()

    while True:
        print("\nRobot Arm Control")
        print("1. Move Servo")
        print("2. Get Servo Position")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            servo_id = int(input("Enter Servo ID (1-6): "))
            position = float(input("Enter position: "))
            arm.set_servo_position(servo_id, position, wait=True)
            print(f"Moved Servo {servo_id} to position {position}")

        elif choice == '2':
            servo_id = int(input("Enter Servo ID (1-6): "))
            position = arm.get_servo_position(servo_id)
            print(f"Servo {servo_id} is at position {position}")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
