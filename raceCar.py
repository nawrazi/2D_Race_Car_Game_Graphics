import pygame as pg
import random
import time 

pg.init()

# initialize the game 

screenWidth = 800
screenHeight = 600

screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Racer")
clock = pg.time.Clock()

pause = False
gameIcon = pg.image.load('gameAssets/logo.png')

pg.display.set_icon(gameIcon)


# codes for all text elements in the game 
playerScore = 0
scoreFont = pg.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

def displayScore(x, y, count):
    renderedScore = scoreFont.render("Score : " + str(count), True, (200, 200, 255))
    screen.blit(renderedScore, (x, y))

overFont = pg.font.Font('freesansbold.ttf', 100)
ScoreFont = pg.font.Font('freesansbold.ttf', 70)
overX = 130
overY = 250
    
def crashMessage(x, y):
    renderedOver = overFont.render("Game Over", True, (255, 0, 0))
    screen.blit(renderedOver, (x, y))

def finalScore(x, y):
    renderedOver = scoreFont.render("Score: " + str(playerScore), True, (255, 0, 0))
    screen.blit(renderedOver, (x, y))


def crashed():

    crashMessage(overX, overY)
    finalScore(overX + 30, overY + 120)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        
        pg.display.update()
        clock.tick(15)

# enemy logic 
enemyImg = pg.image.load('gameAssets/bad.png')
enemyX = random.randint(0, 672) 
enemyY = 20
enemyChangeY = 0



def drawEnemy(x, y):
    screen.blit(enemyImg, (x, y))


#player logic 


playerimg = pg.image.load('gameAssets/good.png')
playerX = 400
playerY = 468

def drawPlayer(x, y):
    screen.blit(playerimg, (x, y))

def movePlayer(event):
    changeX = 0
    if event.type == pg.KEYDOWN:
            # we are pressing down on a key, any key (enter, shift ...)
            if event.key == pg.K_LEFT:
                changeX = -120
            if event.key == pg.K_RIGHT:
                changeX = 120

    if event.type == pg.KEYUP:
        if event.key == pg.K_LEFT or pg.K_RIGHT:
            changeX = 0

    return changeX


def playerBoundary(x):
    if x <= 1:
        x = 1
    if x >= 672:
        x = 672
    return x

#/////////////////////////////////////////// YELLOW LINE ////////////////////////////


# yellowImg = pg.image.load('gameAssets/yellow.png')
# yellowX = 266.66
# yellowY = 1
# yellowChangeY = 0.3

# def drawyellow(x, y):
#     screen.blit(yellowImg, (x, y))


def generateRandom():
    value = random.randint(0, 672)
    return value

carSize = 64

#////////////////////////// INFINITE WHILE LOOP //////////////////////
running = True
while running:
    screen.fill((0, 0, 0))
    
    #////////// KEYBOARD
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        changePlayer = movePlayer(event)
        playerX += changePlayer

   
    

    #//////// PLAYER
    # if playerX > screenWidth - carSize or playerX < 0:
    #     crashed()
    if playerY < enemyY + (carSize * 2):
        if enemyX < playerX < enemyX + carSize or enemyX < playerX + carSize < enemyX + carSize:
            crashed()
    playerX = playerBoundary(playerX)
    drawPlayer(playerX, playerY)



    if enemyY >= 590:
        enemyY = 0 - carSize
        playerScore += 1
        enemyX = generateRandom()

    enemyChangeY = 1
    enemyY += enemyChangeY 
    if enemyY <= 590:
        enemyChangeY = 1
    drawEnemy(enemyX, enemyY)
    displayScore(10, 10, playerScore)

       



    pg.display.update()

