import pygame as pg
import random

class Car:
    """
    A class used to represent the player and enemy cars in the game.

    PARAMETERS
    ----------
    icon : Surface
        The icon displayed on the screen.
    location : tuple<float, float>
        The coordinate location of the car on the screen.
    """
    def __init__(self, icon, location):
        self.icon = pg.image.load(icon)
        self.x, self.y = location
        self.size = 64

class Game:
    """
    A class that contains the contents of the main game screen.

    PARAMETERS
    ----------
    car_color : int
        The color of the car selected at the first screen.

    METHODS
    -------
    displayScore()
        Displays the game score in the top-left corner of the screen.
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

        self.enemy = Car(
            'assets/icons/iconX.png',
            (random.randint(0, 672), 20)
        )

        self.player = Car(
            f'assets/icons/icon{car_color}.png',
            (self.screenWidth / 2, self.screenHeight * 0.75)
        )

    def displayScore(self):
        self.screen.blit(
            self.fonts['score'].render(f'Score: {self.playerScore}', True, (200, 200, 255)),
            (10, 10)
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
        self.enemy.y += 3
        self.screen.blit(self.enemy.icon, (self.enemy.x, self.enemy.y))

    def drawPlayer(self):
        self.screen.blit(self.player.icon, (self.player.x, self.player.y))

    def play(self):
        while True:
            self.screen.fill((250, 240, 230))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.player.x -= 120
                    if event.key == pg.K_RIGHT:
                        self.player.x += 120

            if self.player.y < self.enemy.y + (self.enemy.size * 2):
                if self.enemy.x < self.player.x < self.enemy.x + self.enemy.size:
                    self.crashScreen()
                elif self.enemy.x < self.player.x + self.player.size < self.enemy.x + self.enemy.size:
                    self.crashScreen()

            if not 1 <= self.player.x <= 672:
                self.player.x = 1 if self.player.x < 1 else 672

            if self.enemy.y >= 590:
                self.enemy.y = 0 - self.enemy.size
                self.enemy.x = random.randint(0, 672)
                self.playerScore += 1

            self.drawPlayer()
            self.drawEnemy()
            self.displayScore()

            pg.display.update()
