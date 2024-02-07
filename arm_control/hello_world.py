import xarm

#

    # arm is the first xArm detected which is connected to USB
arm = xarm.Controller('USB')
print('Battery voltage in volts:', arm.getBatteryVoltage())

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)  
servo3 = xarm.Servo(3) 
servo4 = xarm.Servo(4) 
servo5 = xarm.Servo(5) 
servo6 = xarm.Servo(6) 

data = arm.getPosition(servo1, True)
print("servo 1: ",data)
data = arm.getPosition(servo2, True)
print("servo 2: ",data)
data = arm.getPosition(servo3, True)
print("servo 3: ",data)
data = arm.getPosition(servo4, True)
print("servo 4: ",data)
data = arm.getPosition(servo5, True)
print("servo 5: ",data)
data = arm.getPosition(servo6, True)
print("servo 6: ",data)

    # #Vertical Default
    #arm.setPosition([[1, 0.0], [2, 0.0], [3, -90.0], [4, 0.0], [5, 0.0], [6, 0.0]], wait = True)

    # #South Down
    # arm.setPosition([[1, 0.0], [2, 0.0], [3, 0.0], [4, -75.0], [5, 10.0], [6, 0.0]], wait=True)

    # #South West
    # arm.setPosition([[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]], wait=True)

    # #Rotate Claw
    # arm.setPosition([[1, 0.0], [2, 90.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]], wait=True)
    # arm.setPosition([[1, 0.0], [2, -90.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]], wait=True)
    # arm.setPosition([[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]], wait=True)

    # #Open Claw
    # arm.setPosition([[1, 90.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]], wait=True)
    # arm.setPosition([[1, -90.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, -45.0]], wait=True)

    # #South East
    # arm.setPosition([[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]], wait=True)

    # #Rotate Claw
    # arm.setPosition([[1, 0.0], [2, 90.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]], wait=True)
    # arm.setPosition([[1, 0.0], [2, -90.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]], wait=True)
    # arm.setPosition([[1, 0.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]], wait=True)

    # #Open Claw
    # arm.setPosition([[1, 90.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]], wait=True)
    # arm.setPosition([[1, -90.0], [2, 0.0], [3, -45.0], [4, -75.0], [5, 10.0], [6, 45.0]], wait=True)

    # #Vertical Default Setback
    # arm.setPosition([[1, 0.0], [2, 0.0], [3, -90.0], [4, 0.0], [5, 0.0], [6, 0.0]], wait = True)

#if __name__ == "main":
    #hello_world()
