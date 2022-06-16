import pygame as pg
import random

class Game:
    """
    A class that contains the contents of the main game screen.

    PARAMETERS
    ----------
    car_color : int
        The color of the car selected at the first screen.

    METHODS
    -------
    displayScore(x, y)
        Displays the game score at the specified x and y coordinates.
    crashScreen()
        Displays the game over screen with the final score.
    drawEnemy()
        Draws an enemy car at the top of the screen.
     drawPlayer()
        Draws the player car at the center-bottom of the screem.
    play()
        Contains the main loop, handles user input and collision detection.
    """
    def __init__(self, car_color):
        pg.init()
        self.screenWidth = 800
        self.screenHeight = 600

        self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
        pg.display.set_caption('Racer')
        pg.display.set_icon(pg.image.load('assets/icons/logo.png'))

        self.playerScore = 0

        self.fonts = {
            'score': pg.font.SysFont('futura', 30),
            'game_over': pg.font.SysFont('futura', 100)
        }

        self.enemy_icon = pg.image.load('assets/icons/iconX.png')
        self.enemy_x = random.randint(0, 672)
        self.enemy_y = 20

        self.player_icon = pg.image.load(f'assets/icons/icon{car_color}.png')
        self.player_x = self.screenWidth // 2
        self.player_y = self.screenHeight * .75

        self.car_size = 64

    def displayScore(self, x, y):
        self.screen.blit(
            self.fonts['score'].render(f'Score: {self.playerScore}', True, (200, 200, 255)),
            (x, y)
        )

    def crashScreen(self):
        self.screen.blit(
            self.fonts['game_over'].render('Game Over', True, (175, 0, 0)),
            (self.screenWidth // 10, self.screenHeight // 3)
        )
        self.screen.blit(
            self.fonts['score'].render(f'Score: {self.playerScore}', True, (175, 0, 0)),
            (self.screenWidth // 10, (self.screenHeight // 3) + 140)
        )

        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    quit()
            pg.display.update()

    def drawEnemy(self):
        self.enemy_y += 3
        self.screen.blit(self.enemy_icon, (self.enemy_x, self.enemy_y))

    def drawPlayer(self):
        self.screen.blit(self.player_icon, (self.player_x, self.player_y))

    def play(self):
        while True:
            self.screen.fill((250, 240, 230))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.player_x -= 120
                    if event.key == pg.K_RIGHT:
                        self.player_x += 120

            if self.player_y < self.enemy_y + (self.car_size * 2):
                if self.enemy_x < self.player_x < self.enemy_x + self.car_size:
                    self.crashScreen()
                elif self.enemy_x < self.player_x + self.car_size < self.enemy_x + self.car_size:
                    self.crashScreen()

            if not 1 <= self.player_x <= 672:
                self.player_x = 1 if self.player_x < 1 else 672

            if self.enemy_y >= 590:
                self.enemy_y = 0 - self.car_size
                self.enemy_x = random.randint(0, 672)
                self.playerScore += 1

            self.drawPlayer()
            self.drawEnemy()
            self.displayScore(10, 10)

            pg.display.update()
