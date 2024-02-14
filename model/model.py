import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

joints = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 0, 2),
    (0, 0, 3)
]

arm_edges = [
    (0, 1),
    (1, 2),
    (2, 3)
]

def Arm():
    glLineWidth(3)  # Set the line width to 3 pixels
    glBegin(GL_LINES)
    
    colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]  # Red, Green, Blue
    color_index = 0  # Start with the first color
    
    for arm_edge in arm_edges:
        glColor3fv(colors[color_index])  # Set the current color
        for joint in arm_edge:
            glVertex3fv(joints[joint])
        color_index = (color_index + 1) % len(colors)  # Move to the next color, loop back to the start if necessary
    
    glEnd()


def drawGrid():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)  # Set the color to white for the grid lines
    for i in range(-10, 11):
        if i == 0:
            continue  # Skip the axis lines
        # Lines parallel to X-axis
        glVertex3f(-10, -0.1, i)
        glVertex3f(10, -0.1, i)
        # Lines parallel to Z-axis
        glVertex3f(i, -0.1, -10)
        glVertex3f(i, -0.1, 10)
    glEnd()

def rotate_point_around_point(joint_to_rotate, origin_joint, rx, ry, rz): 
    """
    Rotate a point around a given point in 3D space.
    
    :param point: The point to rotate (tuple of floats) -- (x, y, z).
    :param origin: The point around which to rotate the point (tuple of floats) -- (ox, oy, oz).
    :param rx, ry, rz: The rotation angles around the X, Y, and Z axes in radians.
    :return: The rotated point as a tuple (x', y', z').
    """
    
    point = joints[joint_to_rotate]
    origin = joints[origin_joint]
    
    # Translate point to origin
    px, py, pz = point[0] - origin[0], point[1] - origin[1], point[2] - origin[2]

    # Rotate around x-axis
    cos_rx, sin_rx = math.cos(rx), math.sin(rx)
    x = px
    y = cos_rx * py - sin_rx * pz
    z = sin_rx * py + cos_rx * pz

    # Rotate around y-axis
    cos_ry, sin_ry = math.cos(ry), math.sin(ry)
    tmp_x = cos_ry * x + sin_ry * z
    tmp_z = -sin_ry * x + cos_ry * z
    x, z = tmp_x, tmp_z

    # Rotate around z-axis
    cos_rz, sin_rz = math.cos(rz), math.sin(rz)
    tmp_x = cos_rz * x - sin_rz * y
    tmp_y = sin_rz * x + cos_rz * y
    x, y = tmp_x, tmp_y

    # Translate point back
    x_rotated = x + origin[0]
    y_rotated = y + origin[1]
    z_rotated = z + origin[2]

    return x_rotated, y_rotated, z_rotated

# # Example usage
# point = (1, 0, 0)  # Point to rotate
# origin = (0, 0, 0)  # Point around which to rotate
# rx, ry, rz = math.radians(90), math.radians(0), math.radians(0)  # Rotation angles around X, Y, and Z in radians

# rotated_point = rotate_point_around_point(point, origin, rx, ry, rz)
# print(f"Rotated point: {rotated_point}")


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)
    glRotatef(10, 1, 0, 0)  # Adjusted for a better initial view
    
    joints[3] = rotate_point_around_point(3, 2, 0, 20, -30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Arm()
        drawGrid()
        pygame.display.flip()
        pygame.time.wait(10)
        

if __name__ == "__main__":
    main()
