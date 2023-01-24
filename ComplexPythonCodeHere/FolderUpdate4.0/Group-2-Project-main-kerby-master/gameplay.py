import pygame, random
from pygame import mixer

import game_settings
from maingame import Button
from game_settings import default_background

pygame.init()
screen = pygame.display.set_mode((800,600))

ballwav = mixer.Sound("ballhit.wav")
ballwav.set_volume(0.07)
scoremp3 = mixer.Sound("gamescore.mp3")
scoremp3.set_volume(0.09)
pause_sound = pygame.mixer.Sound('pause.wav')
pause_sound.set_volume(0.2)
winner_sound = pygame.mixer.Sound('winner.wav')
winner_sound.set_volume(0.2)

speed = pygame.time.Clock()
gamerun = True  # to run whole game window
gameresume = True  # to toggle pause and resume

# ======== load background images ======== #
bgpng = pygame.image.load(default_background)

# ======== load scores text and game_over functions ======== (see below to find blit text on screen) #
scorefont = pygame.font.Font("munro-small.ttf", 50)
p1score = 0
p2score = 0
scoredisplay = ""

isplayer1won = False
isplayer2won = False

def scorenumbers():
    global ballxd,ballx,bally,p1score,p2score,scoredisplay
    if ballx <= 0:
        scoremp3.play()
        p2score += 1
        ballxd = -2.0 # resets ball speed
        ballx = 386
        bally = 286
        return p1score
    elif ballx+28 >= 800:
        scoremp3.play()
        p1score += 1
        ballxd = 2.0 # resets ball speed
        ballx = 386
        bally = 286
        return p2score

def gameover(a,b):
    global scoredisplay,ballx,ballxd,ballyd,isplayer1won,isplayer2won
    winscore = 10
    if a == winscore:
        scoredisplay = "Player 1 won!!!"
        ballx = 386
        ballxd = 0
        ballyd = 0
        ballpng.set_alpha(0)
        isplayer1won = True
        winner_sound.play()
    elif b == winscore:
        scoredisplay = "Player 2 won!!!"
        ballx = 386
        ballxd = 0
        ballyd = 0
        ballpng.set_alpha(0)
        isplayer2won = True
        winner_sound.play()
    return scoredisplay,isplayer1won,isplayer2won


# ======== Player 1 and 2 images ========== #
player1png = pygame.image.load("tray.png")
player1x = 0
player1y = 268
player1xd = 0
player1yd = 0
def player1(x,y):
    screen.blit(player1png, (x,y))

player2png = pygame.image.load("tray.png")
player2x = 736
player2y = 268
player2xd = 0
player2yd = 0
def player2(x,y):
    screen.blit(player1png, (x,y))

# ======== Ball images ========== #
ballpng = pygame.image.load("ball.png")
ballx = 386
bally = 286
ballserve = [-2.0,2.0]
ballxd = random.choice(ballserve)
ballyd = -1.0
def ball(x,y):
    screen.blit(ballpng,(x,y))
def corner(y):
    global ballyd
    if y <= 0 or y >= 568:
        ballyd *= -1
        ballwav.play()
    return ballyd
def bounce():
    global player1x,player1y,player2x,player2y,ballx,bally,ballxd,ballyd
    if ((ballx <= player1x + 37)and(ballx >= player1x + 28)) and ((bally+28 >= player1y)and(bally <= player1y + 64)):
        ballx = 37
        ballxd *= -1
        if ((bally + 28 >= player1y + 24) and (bally <= player1y + 40)):
            anglenear = [0.3,-0.3,0.5,-0.5]
            ballyd = random.choice(anglenear)
            print(ballyd)
        elif ((bally+28 >= player1y)and(bally <= player1y + 64)):
            anglefar = [1.0,-1.0,1.5,-1.5]
            ballyd = random.choice(anglefar)
            print(ballyd)
        ballxd += 0.2  # increase speed of ball movement
        ballwav.play()

    br = 28 # br means "bottom right"
    if ((ballx+br <= player2x + 37)and(ballx+br >= player2x + 28)) and ((bally+br >= player2y)and(bally <= player2y + 64)):
        ballx = 735
        ballxd *= -1
        if ((bally + 28 >= player2y + 24) and (bally <= player2y + 40)):
            anglenear = [0.3,-0.3,0.5,-0.5]
            ballyd = random.choice(anglenear)
            print(ballyd)
        elif ((bally+28 >= player2y)and(bally <= player2y + 64)):
            anglefar = [1.0,-1.0,1.5,-1.5]
            ballyd = random.choice(anglefar)
            print(ballyd)
        ballxd -= 0.2  # increase speed of ball movement
        ballwav.play()

    return ballyd,ballxd

# to function pause button (spacebar) #
pausefont = pygame.font.Font("munro-small.ttf", 100)
pausetext = pausefont.render("Game paused", False, (100,0,0))
blackimage = pygame.Surface((800,600))
blackimage.fill((50,50,50))
blackimage.set_alpha(10)

def pause(state):
    global gameresume
    if state == True:
        print("game paused")
        pause_sound.play()
        gameresume = False
    else:
        print("game resume")
        pause_sound.play()
        gameresume = True

# ################################################################################################################## #
# ################################################################################################################## #
# ################################################################################################################## #

while gamerun == True:

    gametickspeed = speed.tick(120)  # always tick speed in 120 fps to prevent unexpected fast or slow game speed.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False


        # ======== pressed button ======== #
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1yd = -4.0
            if event.key == pygame.K_s:
                player1yd = 4.0
            if isplayer1won == True:
                if event.key == pygame.K_a:
                    player1xd = -4.0
                if event.key == pygame.K_d:
                    player1xd = 4.0

            if event.key == pygame.K_UP:
                player2yd = -4.0
            if event.key == pygame.K_DOWN:
                player2yd = 4.0
            if isplayer2won == True:
                if event.key == pygame.K_LEFT:
                    player2xd = -4.0
                if event.key == pygame.K_RIGHT:
                    player2xd = 4.0

            # if pressed space then pause #
            if event.key == pygame.K_SPACE:
                pause(gameresume)
            if event.key == pygame.K_ESCAPE:
                gamerun = False

        # ======== released button ======== #
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1yd = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player1xd = 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2yd = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player2xd = 0

    if gameresume == False:
        player1x = player1x
        player1xd = player1xd
        player1y = player1y
        player1yd = player1yd
        player2x = player2x
        player2xd = player2xd
        player2y = player2y
        player2yd = player2yd
        pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(0,0,800,600), 10)
        screen.blit(blackimage,(0,0))
        screen.blit(pausetext, (pausetext.get_rect(center=(400,40))))

        # get the class "Button" in order to make button 3 work (which is back button when paused) #
        button3 = Button('Back', 200, 40, (300, 400), 6)
        button3.draw_button()
        if button3.pressed:
            gamerun = False
        pygame.display.update()

    else:
        # ================== this line and below is to blit images, (from back to front) ====================== #
        screen.fill((0, 0, 0))
        screen.blit(bgpng, (0, 0))

        # display score system #
        scoredisplay = "{} | {}".format(str(p1score).zfill(2), str(p2score).zfill(2))
        gameover(p1score, p2score)

        scoretext = scorefont.render(scoredisplay, False, (100, 100, 100))
        centerposition = scoretext.get_rect(center=(400, 295))
        scorenumbers()
        screen.blit(scoretext, centerposition)

        # display ball and its changed position #
        ballx += ballxd
        bally += ballyd
        corner(bally)
        bounce()
        ball(ballx, bally)

        # display player 1 and 2 and its changed position #
        player1y += player1yd
        player1x += player1xd
        player2y += player2yd
        player2x += player2xd
        if player1y < 0:
            player1y = 0
        elif 536 < player1y:
            player1y = 536
        if player2y < 0:
            player2y = 0
        elif 536 < player2y:
            player2y = 536
        player1(player1x, player1y)
        player2(player2x, player2y)
        pygame.display.update()