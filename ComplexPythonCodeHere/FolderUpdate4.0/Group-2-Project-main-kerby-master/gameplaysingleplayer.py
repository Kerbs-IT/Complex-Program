import pygame, random
from pygame import mixer
from maingame import Button

pygame.init()
screen = pygame.display.set_mode((800,600))
AI_debug = False # enable or disable, developer only

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


# ======================================The AI ARC======================================= #

class PathFinder:
    def __init__(self, yset, offset):
        self.y  = yset + (offset)
        self.realy = yset

    def target(self):
        debug = pygame.draw.rect(screen, (0, 0, 255), [0,(self.y),800,1], 0)
        print(self.y)
        return debug

pos1 = (299,399)
pos2 = (301,401)
class BouncePath():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getpath1(self):
        if 60 > self.x > 40:
            return self.x, self.y
        else:
            return pos1[0], pos1[1]

    def getpath2(self):
        if 120 > self.x > 100:
            return self.x, self.y
        else:
            return pos2[0], pos2[1]

    def lineinter(self, i, j): # to find line intersection
        xdif = (i[0][0] - i[1][0], j[0][0] - j[1][0])
        ydif = (i[0][1] - i[1][1], j[0][1] - j[1][1])

        def detect(a,b):
            return a[0] * b[1] - a[1] * b[0]

        div = detect(xdif, ydif)
        d = (detect(*i), detect(*j))
        try:
            x = detect(d, xdif) / div
        except ZeroDivisionError:
            x = 0
        try:
            y = detect(d, ydif) / div
        except ZeroDivisionError:
            y = 0
        return x,y

    def bouncepath(self, pos1, pos2):
        # print(pos1,pos2)
        if AI_debug:
            pygame.draw.line(screen, "yellow", (pos1), (pos2), 1)


class AI:
    def __init__(self, playery):
        self.playery = playery
        pass

class AIPlayer(AI):
    def __init__(self, playery=300.0, where=300.0): # "where" is a y-coordinate to tell where AI to stop.
        super().__init__(playery)
        self.where = where
    def gopath(self):
        global player2yd # will be removed... this sucks.
        if abs(self.where-self.playery) <= 20:
            player2yd = 0
        elif self.where < self.playery:
            player2yd = -4.0
        elif self.where > self.playery:
            player2yd = 4.0

reaction = 2
class ReactionTime:
    def __init__(self, tick):
        self.tick = tick
    steady = 20
    easy = 1
    hard = 0

    def timer(self):
        print(f"[[[[[[[[[[[[[[[[[[[[[[[[[{self.tick}]]]]]]]]]]]]]]]]]]]]]]")
        if self.tick == 0:
            reset = random.choices([self.hard,self.easy,self.steady], weights=[125,5,1], k=1)
            return reset[0]
        return self.tick - 1


# ========================= Importing =============================== #

ballwav = mixer.Sound("ballhit.wav")
ballwav.set_volume(0.07)
scoremp3 = mixer.Sound("gamescore.mp3")
scoremp3.set_volume(0.09)
pause_sound = pygame.mixer.Sound('pause.wav')
pause_sound.set_volume(0.2)
winner_sound = pygame.mixer.Sound('winner.wav')
winner_sound.set_volume(0.2)
pressed = False

speed = pygame.time.Clock()
gamerun = True  # to run whole game window
gameresume = True  # to toggle pause and resume

# ======== load background images ======== #
bgpng = pygame.image.load("selected_bg.png")
scorep1png = pygame.image.load("background1score.png")
scorep2png = pygame.image.load("background2score.png")

scorep1x = 0
scorep2x = 0
scorep1xd = 0
scorep2xd = 0

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
    global scorep1x, scorep2x, scorep1xd, scorep2xd
    if isplayer1won == True or isplayer2won == True:
        i = 0
    else: i = 128

    scorep1png.set_alpha(i)
    scorep2png.set_alpha(i)
    if turn == 0:
        scorep1x = 0
        scorep2x = 0
        scorep1xd = 0
        scorep2xd = 0
    elif turn == 1:
        screen.blit(scorep2png, (scorep2x, 0))
        scorep2xd = 1
    elif turn == 2:
        screen.blit(scorep1png, (scorep1x, 0))
        scorep1xd = 1
    scorep1x += scorep1xd
    scorep2x -= scorep2xd


def gameover(a,b):
    global scoredisplay,ballx,ballxd,ballyd,isplayer1won,isplayer2won
    winscore = 10
    if a == winscore:
        scoredisplay = "You won!!!"
        ballx = 386
        ballxd = 0
        ballyd = 0
        ballpng.set_alpha(0)
        isplayer1won = True
        winner_sound.play()
    elif b == winscore:
        scoredisplay = "You Lose!!!"
        ballx = 386
        ballxd = 0
        ballyd = 0
        ballpng.set_alpha(0)
        isplayer2won = True
        winner_sound.play()
    return scoredisplay,isplayer1won,isplayer2won


# ======== Player 1 and 2 images ========== #
player1png = pygame.image.load('selected_tray.png')
player1x = 0
player1y = 268
player1xd = 0
player1yd = 0
def player1(x,y):
    screen.blit(player1png, (x,y))

player2png = pygame.image.load("selected_tray.png")
player2x = 736
player2y = 268
player2xd = 0
player2yd = 0
def player2(x,y):
    screen.blit(player1png, (x,y))

# ======== Ball images ========== #
ballpng = pygame.image.load("selected_ball.png")
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
            anglenear = [0.3,-0.3,0.8,-0.8]
            ballyd = random.choice(anglenear)
            print(ballyd)
        elif ((bally+28 >= player1y)and(bally <= player1y + 64)):
            anglefar = [1.3,-1.3,3.5,-3.5]
            ballyd = random.choice(anglefar)
            print(ballyd)
        if ballxd < 8:
            ballxd += 0.2 # increase speed of ball movement
        else:
            ballxd = 8
        ballwav.play()

    br = 28 # br means "bottom right", this is for player2
    if ((ballx+br <= player2x + 37)and(ballx+br >= player2x + 28)) and ((bally+br >= player2y)and(bally <= player2y + 64)):
        ballx = 735
        ballxd *= -1
        if ((bally + 28 >= player2y + 24) and (bally <= player2y + 40)):
            anglenear = [0.3,-0.3,0.8,-0.8]
            ballyd = random.choice(anglenear)
            print(ballyd)
        elif ((bally+28 >= player2y)and(bally <= player2y + 64)):
            anglefar = [1.3,-1.3,3.5,-3.5]
            ballyd = random.choice(anglefar)
            print(ballyd)
        if ballxd < 10:
            ballxd -= 0.2  # increase speed of ball movement
        else:
            ballxd = 10
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

    gametickspeed = speed.tick(170)  # always tick speed lock on 120 fps to prevent unexpected fast or slow game speed.
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
        buttonback = Button('Back', 200, 40, (280, 300), 6)

        buttonback.draw_button()
        if buttonback.pressed:
            pressed = True
        else:
            if pressed == True:
                pressed = False
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

        # THE AI inside resume-only loops #

        target = PathFinder(bally, 14)
        playercord = PathFinder(player2y, 32)

        ballmove = BouncePath(ballx+14,bally+14)
        # if try1.ispath() == True:
        pos1 = ballmove.getpath1()
        pos2 = ballmove.getpath2()

        pos = [pos1,pos2]
        def ydirection():
            if pos[0][1] < pos[1][1]:
                border = [[0, 586], [800, 586]]
            else:
                border = [[0, 14], [800, 14]]
            return border

        # yellow line 1
        linemove = BouncePath(ballx+14,bally+14)
        inter = linemove.lineinter(pos, ydirection())
        linemove.bouncepath(pos1, inter)


        # yellow line 2
        linemove2 = BouncePath(ballx + 14, bally + 14)
        inter2 = linemove2.lineinter((inter,
                                      (inter[0] + (2 / pos[1][0] - pos[0][0]),
                                       inter[1] + (pos[1][1] - pos[0][1]))),
                                     [[0, 14], [800, 14]])
        if inter[1] < 300:
            inter2 = linemove2.lineinter((inter,
                                          (inter[0]+(2/pos[1][0]-pos[0][0]),
                                           inter[1]+(pos[1][1]-pos[0][1]))),
                                         [[0, 586], [800, 586]])
        linemove2.bouncepath(inter, inter2)

        # yellow line 3 # This is an experiment
        linemove3 = BouncePath(ballx + 14, bally + 14)
        inter3 = linemove3.lineinter((inter2,
                                      (inter2[0] - (2 / pos[1][0] - pos[0][0]),
                                       inter2[1] + (pos[1][1] - pos[0][1]))),
                                     [[0, 14], [800, 14]])

        if inter2[1] < 300:
            inter3 = linemove3.lineinter((inter2,
                                          (inter2[0] - (2 / pos[1][0] - pos[0][0]),
                                           inter2[1] + (pos[1][1] - pos[0][1]))),
                                         [[0, 586], [800, 586]])
        linemove3.bouncepath(inter2, inter3)

        print(f"------------------------------{ballxd}---------------------------------")
        vertical_line1 = [[500, 0], [500, 600]]
        if abs(ballxd) >= 3:
            vertical_line1 = [[550, 0], [550, 600]]
        elif abs(ballxd) >= 4:
            vertical_line1 = [[600, 0], [600, 600]]
        elif abs(ballxd) >= 5:
            print("now")
            vertical_line1 = [[620, 0], [620, 600]]
        elif abs(ballxd) >= 6:
            vertical_line1 = [[700, 0], [700, 600]]
        # Predict path 1
        intersectfinal1 = BouncePath(None, None).lineinter((pos1, pos2), vertical_line1)
        predict1cord = PathFinder(intersectfinal1[1], 0)

        # Predict path 2
        intersectfinal2 = BouncePath(None,None).lineinter((inter,inter2),vertical_line1)
        predict2cord = PathFinder(intersectfinal2[1], 0)

        # Predict path 3
        intersectfinal3 = BouncePath(None, None).lineinter((inter2, inter3), vertical_line1)
        predict3cord = PathFinder(intersectfinal3[1], 0)

        def updatepath():
            globals()
            playery_where = playercord.y, random.uniform(predict1cord.y - 100, predict1cord.y + 100)
            which_follow = "[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[predict 1]]]]]]]]]]]]]"
            if not(0 <= intersectfinal1[1] <= 600) and ballx < vertical_line1[0][0]:
                playery_where = playercord.y, random.uniform(predict2cord.y - 100, predict2cord.y + 100)
                which_follow = "[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[predict 2]]]]]]]]]]]]]"
            if not(0 <= intersectfinal1[1] <= 600) and not(0 <= intersectfinal2[1] <= 600) and ballx < vertical_line1[0][0]:
                playery_where = playercord.y, random.uniform(predict3cord.y - 100, predict3cord.y + 100)
                which_follow = "[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[predict 3]]]]]]]]]]]]]"
            elif ballx >= vertical_line1[0][0]:
                playery_where = playercord.y, random.uniform(target.y-0,target.y+0)
                which_follow = "[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[GET BALL FAST]]]]]]]]]]]]]"
            return playery_where, which_follow

        # reaction time for AI #
        React = ReactionTime(reaction)
        reaction = React.timer()
        if reaction == 0:
            playery = updatepath()[0][0]
            where = updatepath()[0][1]
            player2control = AIPlayer(playery, where)
        else:
            player2control = AIPlayer()
        print(updatepath()[1])
        player2control.gopath()

        # IF show AI debug is true
        if AI_debug == True:

            target.target()
            playercord.target()
            predict1cord.target()
            predict2cord.target()

            pygame.draw.rect(screen, (250,128,114), [inter[0]-5, inter[1]-5, 10, 10], 0)
            pygame.draw.rect(screen, (250, 128, 114), [inter2[0] - 5, inter2[1] - 5, 10, 10], 0)
            pygame.draw.rect(screen, (250, 128, 114), [inter3[0] - 5, inter3[1] - 5, 10, 10], 0)

            pygame.draw.rect(screen, (250, 128, 114), [vertical_line1[0][0] - 5, vertical_line1[0][1] - 5, 5, 600], 0)
            pygame.draw.rect(screen, (250, 208, 114), [intersectfinal1[0] - 5, intersectfinal1[1] - 5, 20, 20], 0)
            pygame.draw.rect(screen, (250, 208, 114), [intersectfinal2[0] - 5, intersectfinal2[1] - 5, 20, 20], 0)
            pygame.draw.rect(screen, (250, 208, 114), [intersectfinal3[0] - 5, intersectfinal3[1] - 5, 20, 20], 0)

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