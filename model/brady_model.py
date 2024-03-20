import pygame
from pygame.locals import *
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

def draw_scene():
    draw_cylinder(0, 5, -55, (0.5, 1.0, 0.5), 0, (0, 1, 0))
    draw_cylinder(0, 5, -47, (0.5, 0.5, 1.0), 0, (0, 1, 0))
    draw_cylinder(0, 5, -39, (0, 0, 1.0), 0, (0, 1, 0))
    draw_claw(-0.5, 5, -31, (1.0, 1.0, 0), -45, (0, 1, 0))
    draw_claw(0.5, 5, -31, (1.0, 1.0, 0), 45, (0, 1, 0))
    draw_rectangle()

def main():
    global last_mouse_position, yaw, pitch

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 60.0)
    glTranslatef(0.0, 40, initial_zoom)
    glRotatef(-90, 1, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-20, 0, 0, 1)
                elif event.key == pygame.K_RIGHT:
                    glRotatef(20, 0, 0, 1)                  

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        draw_scene()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
