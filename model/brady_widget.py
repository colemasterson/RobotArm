import math
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from cam_position.normalization import getPositionData, transformCameraCoordinates
# from positions need to get values some how.




yaw, pitch = 0, 0
initial_zoom = -55


update_armPositionsData =[[ 0.,      0.,        0.        ],
  [-0.02083994,  0.03558095, -0.21626294],
  [-0.27997975,  0.02595508, -0.41643387]]

update_angles = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, -90.0, 0.0)]

firstSegmentEulerAngle = (0.0, 0.0, 0.0)
secondSegmentEulerAngle = (0.0, 0.0, 0.0)
thirdSegmentEulerAngle = (0.0, 0.0, 0.0)


class Position:
    def __init__(self, x:float, y:float, z:float):
        self.x:float = x
        self.y:float = y
        self.z:float = z


armPositionsData = [
    Position(0.0, 0.0, 0.0),
    Position(0.0, 0.0, 0.0),
    Position(0.0, 0.0, 0.0)
]


class ArmPositions:
    def __init__(self, positions):
        self.position1 = Position(positions[0].x, positions[0].y, positions[0].z)
        self.position2 = Position(positions[1].x, positions[1].y, positions[1].z)
        self.position3 = Position(positions[2].x, positions[2].y, positions[2].z)




    def scale(self, x_factor, y_factor, z_factor):
        scaled_position1 = Position(self.position1.x * x_factor, self.position1.y * y_factor, self.position1.z * z_factor)
        scaled_position2 = Position(self.position2.x * x_factor, self.position2.y * y_factor, self.position2.z * z_factor)
        scaled_position3 = Position(self.position3.x * x_factor, self.position3.y * y_factor, self.position3.z * z_factor)
        return ArmPositions([scaled_position1, scaled_position2, scaled_position3])


    def addOffset(self):
        offset_position1 = Position(self.position1.x, self.position1.y + 5, self.position1.z - 54)
        offset_position2 = Position(self.position2.x, self.position2.y + 5, self.position2.z - 54)
        offset_position3 = Position(self.position3.x, self.position3.y + 5, self.position3.z - 54)
        return ArmPositions([offset_position1, offset_position2, offset_position3])




class EulerAngles:
    def __init__(self, x_degrees, y_degrees, z_degrees):
        self.x_degrees = x_degrees + 180
        self.y_degrees = y_degrees
        self.z_degrees = z_degrees


def update_positions_and_angles(new_positions, new_angles):
    global armPositionsData, firstSegmentEulerAngle, secondSegmentEulerAngle, thirdSegmentEulerAngle
    armPositionsData = [Position(*pos) for pos in new_positions]

    firstSegmentEulerAngle = new_angles[0]
    secondSegmentEulerAngle = new_angles[1]
    thirdSegmentEulerAngle = new_angles[2]


# Define rotation matrices for x, y, and z axes
def rotation_matrix_x(angle):
    rad = math.radians(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(rad), -math.sin(rad), 0],
        [0, math.sin(rad), math.cos(rad), 0],
        [0, 0, 0, 1]
    ])


def rotation_matrix_y(angle):
    rad = math.radians(angle)
    return np.array([
        [math.cos(rad), 0, math.sin(rad), 0],
        [0, 1, 0, 0],
        [-math.sin(rad), 0, math.cos(rad), 0],
        [0, 0, 0, 1]
    ])


def rotation_matrix_z(angle):
    rad = math.radians(angle)
    return np.array([
        [math.cos(rad), -math.sin(rad), 0, 0],
        [math.sin(rad), math.cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])




def draw_cylinder(x, y, z, color, eAngle: EulerAngles):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)


    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)


    
    # Apply rotations
    rotation_matrix = np.dot(rotation_matrix_z(eAngle.z_degrees),
                              np.dot(rotation_matrix_y(eAngle.y_degrees),
                                     rotation_matrix_x(eAngle.x_degrees)))
    glMultMatrixf(rotation_matrix)


    gluCylinder(quadric, 2, 2, 8, 32, 1)
    glPopMatrix()




def draw_cylinder_small(x, y, z, color, eAngle: EulerAngles):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)


    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)
    
    # Apply rotations
    rotation_matrix = np.dot(rotation_matrix_z(eAngle.z_degrees),
                              np.dot(rotation_matrix_y(eAngle.y_degrees),
                                     rotation_matrix_x(eAngle.x_degrees)))
    glMultMatrixf(rotation_matrix)


    gluCylinder(quadric, 2, 2, 4, 32, 1)
    glPopMatrix()
    
    end_point = np.array([0, 0, 4, 1])  # Representing the point in homogeneous coordinates


# Apply rotation to the height vector
    end_point = np.dot(rotation_matrix, end_point)


# Extract x, y, z values from the transformed point
    end_x, end_y, end_z, _ = end_point


    end_x =  x - end_x 
    end_y =  y + end_y
    end_z =  z + end_z


    
    return end_x, end_y, end_z




def draw_claw(x, y, z, color, eAngle: EulerAngles):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)


    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)




    rotation_matrix = np.dot(rotation_matrix_z(eAngle.z_degrees),
                              np.dot(rotation_matrix_y(eAngle.y_degrees),
                                     rotation_matrix_x(eAngle.x_degrees)))
    glMultMatrixf(rotation_matrix)


    gluCylinder(quadric, 1, 0.5, 5, 32, 1)
    glPopMatrix()
    
def draw_rectangle():
    glPushMatrix()
    glColor3f(1.0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(-4, 0, initial_zoom)
    glVertex3f(4, 0, initial_zoom)
    glVertex3f(4, 10, initial_zoom)
    glVertex3f(-4, 10, initial_zoom)
    glEnd()
    glPopMatrix()
    
# def draw_octagon():
#     glPushMatrix()
#     glColor3f(1.0, 0, 0)
#     glBegin(GL_LINES)
#     glVertex3f(-4, 0, initial_zoom)
#     glVertex3f(4, 0, initial_zoom)

#     glVertex3f(4, 0, initial_zoom)
#     glVertex3f(4, 10, initial_zoom)

#     glVertex3f(4, 10, initial_zoom)
#     glVertex3f(-4, 10, initial_zoom)

#     glVertex3f(-4, 10, initial_zoom)
#     glVertex3f(-4, 0, initial_zoom)

#     glVertex3f(-4, 0, initial_zoom)
#     glVertex3f(-4, 0, initial_zoom + 1)

#     glVertex3f(4, 0, initial_zoom)
#     glVertex3f(4, 0, initial_zoom + 1)

#     glVertex3f(4, 10, initial_zoom)
#     glVertex3f(4, 10, initial_zoom + 1)

#     glVertex3f(-4, 10, initial_zoom)
#     glVertex3f(-4, 10, initial_zoom + 1)

#     glVertex3f(-4, 0, initial_zoom + 1)
#     glVertex3f(4, 0, initial_zoom + 1)

#     glVertex3f(4, 0, initial_zoom + 1)
#     glVertex3f(4, 10, initial_zoom + 1)

#     glVertex3f(4, 10, initial_zoom + 1)
#     glVertex3f(-4, 10, initial_zoom + 1)

#     glVertex3f(-4, 10, initial_zoom + 1)
#     glVertex3f(-4, 0, initial_zoom + 1)
#     glEnd()
#     glPopMatrix()

def draw_octagon():
    glPushMatrix()
    glColor3f(1.0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(-4, 0, initial_zoom)
    glVertex3f(-2.828, 0, initial_zoom + 2.828)

    glVertex3f(-2.828, 0, initial_zoom + 2.828)
    glVertex3f(2.828, 0, initial_zoom + 2.828)

    glVertex3f(2.828, 0, initial_zoom + 2.828)
    glVertex3f(4, 0, initial_zoom)

    glVertex3f(4, 0, initial_zoom)
    glVertex3f(2.828, 0, initial_zoom - 2.828)

    glVertex3f(2.828, 0, initial_zoom - 2.828)
    glVertex3f(-2.828, 0, initial_zoom - 2.828)

    glVertex3f(-2.828, 0, initial_zoom - 2.828)
    glVertex3f(-4, 0, initial_zoom)

    glVertex3f(-4, 0, initial_zoom)
    glVertex3f(-2.828, 0, initial_zoom + 2.828)

    glVertex3f(-2.828, 0, initial_zoom + 2.828)
    glVertex3f(2.828, 0, initial_zoom + 2.828)

    glVertex3f(2.828, 0, initial_zoom + 2.828)
    glVertex3f(4, 0, initial_zoom)

    glVertex3f(4, 0, initial_zoom)
    glVertex3f(2.828, 0, initial_zoom - 2.828)

    glVertex3f(2.828, 0, initial_zoom - 2.828)
    glVertex3f(-2.828, 0, initial_zoom - 2.828)

    glVertex3f(-2.828, 0, initial_zoom - 2.828)
    glVertex3f(-4, 0, initial_zoom)
    glEnd()
    glPopMatrix()

    


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)  # Enable the widget to receive focus
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)  # update at fps of 100
        self.rotation_angle = 0




    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        gluPerspective(45, (800 / 600), 0.1, 70.0)
        glTranslatef(0.0, 40, initial_zoom)
        glRotatef(-90, 1, 0, 0)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation_angle, 0, 0, 1)
        
        tvecs, rvecs = getPositionData()
        # Flag to tell if using x or y axis, x - true, y - false
        p_x_or_y = True
        transformed_points = transformCameraCoordinates(tvecs, p_x_or_y)
        
        # print("POINTS: \n", transformed_points, "\n")
        # print("ROTATIONS: \n", rvecs, "\n")
        
        update_positions_and_angles(transformed_points, rvecs)
        
        # print("First Segment Euler Angle:", firstSegmentEulerAngle)
        print("Second Segment Euler Angle:", secondSegmentEulerAngle)
        print("Third Segment Euler Angle:", thirdSegmentEulerAngle)
        
        armPositions = ArmPositions(armPositionsData)
        armPositions = armPositions.scale(1, 1, -40)
        armPositions = armPositions.addOffset()
        
        position1: Position = armPositions.position1
        position2: Position = armPositions.position2
        position3: Position = armPositions.position3
        
        firstEulerAngle = EulerAngles(*firstSegmentEulerAngle)
        draw_cylinder(position1.x, position1.y, position1.z, (1.0, 0, 0), firstEulerAngle)
        
        secondEulerAngle = EulerAngles(*secondSegmentEulerAngle)
        draw_cylinder(position2.x, position2.y, position2.z, (0, 1.0, 0), secondEulerAngle)
        
        thirdEulerAngle = EulerAngles(*thirdSegmentEulerAngle)
        x,y,z = draw_cylinder_small(position3.x, position3.y, position3.z, (0, 0, 1.0), thirdEulerAngle)
        
        claw1_rotation = EulerAngles(thirdEulerAngle.x_degrees, 45 + thirdEulerAngle.y_degrees, thirdEulerAngle.z_degrees)
        claw2_rotation = EulerAngles(thirdEulerAngle.x_degrees, -45 + thirdEulerAngle.y_degrees, thirdEulerAngle.z_degrees)
        
        # draw_claw(x, y, z, (0, 0, 1.0),claw1_rotation)
        # draw_claw(x, y, z, (0, 0, 1.0), claw2_rotation)


        draw_rectangle()
        #draw_octagon()
        glPopMatrix()


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.rotation_angle += -20
        elif event.key() == Qt.Key_Right:
            self.rotation_angle += 20
        self.update()
        
    # tvec - Translation Vector
    # rvec - Rotation Vector
    def getVectors(self, tvec, rvec):
        a = 3
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.openglWidget = OpenGLWidget(self)
        self.setCentralWidget(self.openglWidget)
        self.setWindowTitle("OpenGL within PyQt5")
        self.setGeometry(100, 100, 800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
