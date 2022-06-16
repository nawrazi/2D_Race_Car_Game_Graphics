from pygame.constants import *
from OpenGL.GLU import *
from utils.loader import *
import random

class CarSelector:

    def __init__(self):
        pygame.init()
        self.viewport = (800, 600)
        self.surface = pygame.display.set_mode(self.viewport, OPENGL | DOUBLEBUF)
        pygame.display.set_caption('Car Selection')
        glClearColor(.98, .94, .9, 0)

        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        self.cur_color = 3
        self.all_skins = 7
        self.model = Loader('assets/model/porsche.obj', color=self.cur_color)

    def draw(self, new_color=None):
        if new_color is not None:
            self.cur_color = new_color
            self.model = Loader('assets/model/porsche.obj', color=self.cur_color)
            glCallList(self.model.gl_list)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90.0, self.viewport[0]/self.viewport[1], 0.1, 50.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

        glCallList(self.model.gl_list)

    def menu(self):
        text_color = ((0, 0, 0, 255), (250, 240, 230, 0))
        font = pygame.font.SysFont('futura', 16)

        change_color_text = font.render('< Change Color >', True, *text_color)
        random_color_text = font.render('R - Random Color', True, *text_color)
        enter_game_text = font.render('ENTER - Start Game', True, *text_color)

        change_color_data = pygame.image.tostring(change_color_text, "RGBA", True)
        glWindowPos2d(10, 50)
        glDrawPixels(
            change_color_text.get_width(), change_color_text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, change_color_data
        )

        random_color_data = pygame.image.tostring(random_color_text, "RGBA", True)
        glWindowPos2d(10, 30)
        glDrawPixels(
            random_color_text.get_width(), random_color_text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, random_color_data
        )

        enter_game_data = pygame.image.tostring(enter_game_text, "RGBA", True)
        glWindowPos2d(10, 10)
        glDrawPixels(
            enter_game_text.get_width(), enter_game_text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, enter_game_data
        )

    def run(self):
        rx, ry, rz = 0, 0, 0
        rotate = False

        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    quit()

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return self.cur_color

                    if e.key == pygame.K_r:
                        new_color = random.randint(0, self.all_skins - 1)
                        while new_color == self.cur_color:
                            new_color = random.randint(0, self.all_skins - 1)
                        self.draw(new_color)

                    elif e.key == pygame.K_LEFT:
                        new_color = self.cur_color - 1 if self.cur_color > 0 else self.all_skins - 1
                        self.draw(new_color)

                    elif e.key == pygame.K_RIGHT:
                        new_color = (self.cur_color + 1) % self.all_skins
                        self.draw(new_color)

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
            self.menu()
            self.draw()

            pygame.display.flip()
            pygame.time.wait(10)
