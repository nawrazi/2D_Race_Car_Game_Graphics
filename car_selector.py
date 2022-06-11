from pygame.constants import *
from OpenGL.GLU import *
from loader import *

pygame.init()
viewport = (800, 600)
pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
pygame.display.set_caption('Car Color Selection')

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)

model = Loader('model/porsche.obj', car_color=1)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(90.0, viewport[0]/viewport[1], 0.1, 50.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry, rz = 0, 0, 0
rotate = False

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            quit()
        elif e.type == MOUSEBUTTONDOWN:
            rotate = True
        elif e.type == MOUSEBUTTONUP:
            rotate = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx -= j
                ry += j
                rz += i

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslate(0, -0.2, -3.5)
    glRotate(ry - 50, 1, 0, 0)
    glRotate(rz - 90, 0, 0, 1)
    glRotate(rx - 40, 0, 1, 0)
    glCallList(model.gl_list)

    pygame.display.flip()
    pygame.time.wait(10)
