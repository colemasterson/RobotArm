import xarm

# Servos Value Ranges
# 1 - (?, ?) - Claw
# 2 - (?, ?) - Claw Rotate
# 3 - (?, ?)
# 4 - (?, ?)
# 5 - (?, ?)
# 6 - (?, ?) - Base Rotation


def open(arm):
    arm.setPosition(1, -90.0, wait=True)
    
def close(arm):
    arm.setPosition(1, 90.0, wait=True)

def up(arm):
    arm.setPosition([[1, 0.0], [2, 0.0], [3, -90.0], [4, 0.0], [5, 0.0], [6, 0.0]], wait = True)
    
def down(arm):
    arm.setPosition(5, 650, wait=True)
    arm.setPosition(3, 1000, wait=True)
    arm.setPosition(4, 700, wait=True)
    arm.setPosition(5, 800, wait=True)
    open(arm)
    close(arm)
 
def forwards(arm):
    arm.setPosition(6, 0.0, wait=True)
    arm.setPosition(4, 1000, wait=True)
    
def backwards(arm):
    arm.setPosition(6, 0.0, wait=True)
    arm.setPosition(4, 0, wait=True)
    
def left(arm):
    arm.setPosition(6, -90.0, wait=True)
    arm.setPosition(4, 0, wait=True)   

def right(arm):
    arm.setPosition(6, 90.0, wait=True)
    arm.setPosition(4, 0, wait=True)

####################    Driver   ####################
    
# arm is the first xArm detected which is connected to USB
arm = xarm.Controller('USB')
print('Battery voltage in volts:', arm.getBatteryVoltage())

# Initialize the Servos motors
servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)  
servo3 = xarm.Servo(3) 
servo4 = xarm.Servo(4) 
servo5 = xarm.Servo(5) 
servo6 = xarm.Servo(6) 

up(arm)
open(arm)
close(arm)
forwards(arm)
up(arm)
backwards(arm)
up(arm)
left(arm)
up(arm)
right(arm)
up(arm)
down(arm)
up(arm)
