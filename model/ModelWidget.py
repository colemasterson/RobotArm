from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer, QPoint, Qt
from PyQt5.QtGui import QMouseEvent
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)  # Use update to trigger paintGL
        self.timer.start(16)  # Approximate target of 60fps

        self.lastPos = QPoint()
        self.camera_angle = [10, 0]  # Initial camera angles

        # Initial joint positions and edges (adapted from the given script)
        self.joints = [
            (0, 0, 0),
            (0, 0, 1),
            (0, 0, 2),
            (0, 0, 3)
        ]
        self.arm_edges = [
            (0, 1),
            (1, 2),
            (2, 3)
        ]

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Adjust the view using the camera angles
        gluLookAt(
            math.sin(math.radians(self.camera_angle[1])) * 10, 
            self.camera_angle[0], 
            math.cos(math.radians(self.camera_angle[1])) * 10, 
            0, 0, 0, 
            0, 1, 0
        )

        self.draw_arm()
        self.draw_grid()

    def draw_cylinder_between_points(self, p1, p2, radius):
        dx, dy, dz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
        length = math.sqrt(dx**2 + dy**2 + dz**2)

        glPushMatrix()
        glTranslatef(p1[0], p1[1], p1[2])

        if length != 0:
            ax = 180 * math.acos(dz/length) / math.pi
            rx, ry = -dy * dz, dx * dz
            glRotatef(ax, rx, ry, 0.0)

        quadric = gluNewQuadric()
        gluCylinder(quadric, radius, radius, length, 32, 1)
        glPopMatrix()

    def draw_arm(self):
        colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
        color_index = 0
        radius = 0.05
        for edge in self.arm_edges:
            glColor3fv(colors[color_index])
            p1, p2 = self.joints[edge[0]], self.joints[edge[1]]
            self.draw_cylinder_between_points(p1, p2, radius)
            color_index = (color_index + 1) % len(colors)

    def draw_grid(self):
        glLineWidth(1)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for i in range(-10, 11):
            glVertex3f(-10, 0, i)
            glVertex3f(10, 0, i)
            glVertex3f(i, 0, -10)
            glVertex3f(i, 0, 10)
        glEnd()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.camera_angle[1] += dx * 0.5
            self.camera_angle[0] += dy * 0.5

        self.lastPos = event.pos()
        self.update()
