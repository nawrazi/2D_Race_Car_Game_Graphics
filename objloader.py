import pygame
from OpenGL.GL import *

class OBJ:
    def __init__(self, filename, car_color):
        if not 1 <= car_color <= 5:
            raise Exception("Invalid color selection")

        self.car_color = car_color
        self.vertices = []
        self.normals = []
        self.textures = []
        self.faces = []
        self.gl_list = 0
        self.mtl = {}

        for line in open(filename):
            values = line.split()
            if not values:
                continue
            tag = values[0]

            if tag == 'v':
                v = list(map(float, values[1:4]))
                v[1], v[2] = v[2], v[1]
                self.vertices.append(v)

            elif tag == 'vn':
                v = list(map(float, values[1:4]))
                v[1], v[2] = v[2], v[1]
                self.normals.append(v)

            elif tag == 'vt':
                self.textures.append(list(map(float, values[1:3])))

            elif tag == 'f':
                faces, textures, norms = [], [], []
                for v in values[1:]:
                    w = v.split('/')
                    faces.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        textures.append(int(w[1]))
                    else:
                        textures.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)

                self.faces.append((faces, norms, textures))

        self.loadTexture()
        self.generate()

    def loadTexture(self):
        surface = pygame.image.load(f'model/skin{self.car_color}/0000.BMP')
        image = pygame.image.tostring(surface, 'RGBA', True)
        ix, iy = surface.get_rect().size
        texture_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

        self.mtl['texture_Kd'] = texture_id

    def generate(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for vertices, normals, textures in self.faces:
            glBindTexture(GL_TEXTURE_2D, self.mtl['texture_Kd'])
            glBegin(GL_POLYGON)

            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if textures[i] > 0:
                    glTexCoord2fv(self.textures[textures[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])

            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()
