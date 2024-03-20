import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *

yaw, pitch = 0, 0
initial_zoom = -55

def draw_cylinder(x, y, z, color, rotation_angle, rotation_axis):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)

    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, *rotation_axis)
    gluCylinder(quadric, 2, 2, 8, 32, 1)
    glPopMatrix()

def draw_claw(x, y, z, color, rotation_angle, rotation_axis):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)

    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, *rotation_axis)
    gluCylinder(quadric, 1, 0.5, 6, 32, 1)
    glPopMatrix()

def draw_rectangle():
    glPushMatrix()
    glColor3f(1.0, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-4, 0, initial_zoom)
    glVertex3f(4, 0, initial_zoom)
    glVertex3f(4, 10, initial_zoom)
    glVertex3f(-4, 10, initial_zoom)
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
        gluPerspective(45, (800 / 600), 0.1, 60.0)
        glTranslatef(0.0, 40, initial_zoom)
        glRotatef(-90, 1, 0, 0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(self.rotation_angle, 0, 0, 1)
        draw_rectangle()
        draw_cylinder(0, 5, -55, (0.5, 1.0, 0.5), 0, (0, 1, 0))
        draw_cylinder(0, 5, -47, (0.5, 0.5, 1.0), 0, (0, 1, 0))
        draw_cylinder(0, 5, -39, (0, 0, 1.0), 0, (0, 1, 0))
        draw_claw(-0.5, 5, -31, (1.0, 1.0, 0), -45, (0, 1, 0))
        draw_claw(0.5, 5, -31, (1.0, 1.0, 0), 45, (0, 1, 0))
        glPopMatrix()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.rotation_angle += -20
        elif event.key() == Qt.Key_Right:
            self.rotation_angle += 20
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
