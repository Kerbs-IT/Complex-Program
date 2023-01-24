import pygame, random
from pygame import mixer
from maingame import Button

pygame.init()
screen = pygame.display.set_mode((800,600))

# ===============================CLASS====================================== #
# this is update for complex #
class ServeGoaledBall:
    def __init__(self,ballx,bally):
        self.ballx = ballx
        self.bally = bally

class Playerserve(ServeGoaledBall):
    def __init__(self, ballx, bally, xoffset, playery):
        super().__init__(ballx, bally)
        self.xoffset = xoffset
        self.playery = playery

    def holdplayer(self):
        self.ballx = self.xoffset
        self.bally = self.playery + 18 # this plus 18 helps to center the ball from the tray image so don't change
        return self.ballx, self.bally

defaulttick = 200
tick = defaulttick
class ServeTime:
    def __init__(self, tick):
        self.servetime = tick

    def timer(self):
        return self.servetime - 1

# ball trail effect #
class BallRayEffect:
    def __init__(self,ballx,bally):
        self.ballx = ballx
        self.bally = bally

    effectx = [0,1,2,3,4,5,6,7,8,9,10]
    effecty = [0,1,2,3,4,5,6,7,8,9,10]

    def assign(self):
        for i in range(10,0-1,-1):
            if i != 0:
                BallRayEffect.effectx[i] = BallRayEffect.effectx[i - 1]
                BallRayEffect.effecty[i] = BallRayEffect.effecty[i - 1]
                # print(ballrayeffect.effectx)
            elif i == 0:
                BallRayEffect.effectx[i] = self.ballx
                BallRayEffect.effecty[i] = self.bally

    def start(self):
        for i in range(10,0-1,-1):
            if isplayer1won == True or isplayer2won == True:
                balleffectpng.set_alpha(0)
            else:
                balleffectpng.set_alpha(128/(i+1))
            screen.blit(balleffectpng, (BallRayEffect.effectx[i], BallRayEffect.effecty[i]))



# ========================================================================== #

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
bgpng = pygame.image.load("background.png")
scorep1png = pygame.image.load("background1score.png")
scorep2png = pygame.image.load("background2score.png")

# ======== load scores text and game_over functions ======== (see below to find blit text on screen) #
scorefont = pygame.font.Font("munro-small.ttf", 50)
p1score = 0
p2score = 0
scoredisplay = ""

isplayer1won = False
isplayer2won = False

def scorenumbers(): #This function helps to teleport ball if ball hits the goal.
    global turn,ballxd,ballx,bally,p1score,p2score,scoredisplay
    if ballx <= 0:
        turn = 1
        scoremp3.play()
        p2score += 1
        ballxd = 0 # resets ball speed
        # ballx = 386
        # bally = 286
        return p1score, turn
    elif ballx+28 >= 800:
        turn = 2
        scoremp3.play()
        p1score += 1
        ballxd = 0 # resets ball speed
        # ballx = 386
        # bally = 286
        return p2score, turn
turn = 0

def ScoreAnimation():
    global scoretick
    if isplayer1won == True or isplayer2won == True:
        i = 0
    else: i = 128

    scorep2png.set_alpha(i)
    if turn == 1:
        screen.blit(scorep2png, (0, 0))
    elif turn == 2:
        screen.blit(scorep1png, (0, 0))
scoretick = 0

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
balleffectpng = pygame.image.load("balleffect.png")
ballx = 386
bally = 286
ballserve = [-3.0,3.0]
ballxd = random.choice(ballserve)
ballyd = -1.0
def ball(x,y):
    brf = BallRayEffect(ballx,bally)
    brf.assign()
    brf.start()
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
            anglenear = [0.3,-0.3,0.7,-0.7]
            ballyd = random.choice(anglenear)
            print(ballyd)
        elif ((bally+28 >= player1y)and(bally <= player1y + 64)):
            anglefar = [1.0,-1.0,2.5,-2.5]
            ballyd = random.choice(anglefar)
            print(ballyd)
        if ballxd < 13: ballxd += 0.2 # increase speed of ball movement
        else: ballxd = 13
        ballwav.play()

    br = 28 # br means "bottom right", this is for player2
    if ((ballx+br <= player2x + 37)and(ballx+br >= player2x + 28)) and ((bally+br >= player2y)and(bally <= player2y + 64)):
        ballx = 735
        ballxd *= -1
        if ((bally + 28 >= player2y + 24) and (bally <= player2y + 40)):
            anglenear = [0.3,-0.3,0.7,-0.7]
            ballyd = random.choice(anglenear)
            print(ballyd)
        elif ((bally+28 >= player2y)and(bally <= player2y + 64)):
            anglefar = [1.0,-1.0,2.5,-2.5]
            ballyd = random.choice(anglefar)
            print(ballyd)
        if ballxd < 13: ballxd -= 0.2  # increase speed of ball movement
        else: ballxd = 13
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

    gametickspeed = speed.tick(220)  # always tick speed lock on 220 fps to prevent unexpected fast or slow game speed.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False


        # ======== pressed button ======== #
        if event.type == pygame.KEYDOWN:

            # player-serve buttons
            if turn == 1:
                if event.key == pygame.K_LSHIFT:
                    ballxd = 2.0
                    turn = 0
                    tick = defaulttick

            elif turn == 2:
                if event.key == pygame.K_RSHIFT:
                    ballxd = -2.0
                    turn = 0
                    tick = defaulttick


            # player-movement buttons
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

    else: # if gameresume is now true or if game is not pause... this line below will trigger continously #
        # ================== this line and below is to blit images, (from back to front) ====================== #
        screen.fill((0, 0, 0))
        screen.blit(bgpng, (0, 0))

        # display score system #
        scoredisplay = "{} | {}".format(str(p1score).zfill(2), str(p2score).zfill(2))
        gameover(p1score, p2score)

        scoretext = scorefont.render(scoredisplay, False, (100, 100, 100))
        centerposition = scoretext.get_rect(center=(400, 295))
        scorenumbers()
        ScoreAnimation()
        screen.blit(scoretext, centerposition)

        # display ball and its changed position #
        ballx += ballxd
        bally += ballyd
        corner(bally)
        bounce()
        ball(ballx, bally)

        if turn != 0:
            print(tick)
            timer = ServeTime(tick)
            tick = timer.timer()
            if turn == 1:
                ballscene = Playerserve(ballx, bally, 38, player1y)
                ballscene.holdplayer()
                ballx,bally = ballscene.ballx,ballscene.bally
                if timer.timer() == 0:
                    ballxd = 2.0
                    turn = 0
                    tick = defaulttick

            elif turn == 2:
                ballscene = Playerserve(ballx, bally, 734, player2y)
                ballscene.holdplayer()
                ballx, bally = ballscene.ballx, ballscene.bally
                if timer.timer() == 0:
                    ballxd = -2.0
                    turn = 0
                    tick = defaulttick


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