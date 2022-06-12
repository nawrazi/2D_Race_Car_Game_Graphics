from pygame.constants import *
from OpenGL.GLU import *
from loader import *
import random

class CarSelector:

    def __init__(self):
        pygame.init()
        self.viewport = (800, 600)
        self.surface = pygame.display.set_mode(self.viewport, OPENGL | DOUBLEBUF)
        pygame.display.set_caption('Car Selection')

        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        self.cur_color = 1
        self.model = Loader('model/porsche.obj', color=self.cur_color)

    def draw(self, new_color=None):
        if new_color:
            self.cur_color = new_color
            self.model = Loader('model/porsche.obj', color=self.cur_color)
            glCallList(self.model.gl_list)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90.0, self.viewport[0]/self.viewport[1], 0.1, 50.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

        glCallList(self.model.gl_list)

    def run(self):
        rx, ry, rz = 0, 0, 0
        rotate = False

        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    quit()

                elif e.type == pygame.KEYDOWN:
                    if e.key == 13:
                        return self.cur_color

                    new_color = random.randint(0, 5)
                    while new_color == self.cur_color:
                        new_color = random.randint(0, 5)

                    self.draw(new_color)
                    continue

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
            glCallList(self.model.gl_list)
            self.draw()

            pygame.display.flip()
            pygame.time.wait(10)
