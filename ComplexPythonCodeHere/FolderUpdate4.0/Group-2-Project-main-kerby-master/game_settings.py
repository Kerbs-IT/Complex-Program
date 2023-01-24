import pygame
from maingame import Button
import os
# Initialize pygame
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('volume slider')

# create a variable that store the volume level
if os.path.exists('volume.txt'):
    with open('volume.txt','r') as f:
        background_volume = float(f.read())*100
        background_volume = int(background_volume)
else:
    background_volume = 50

# create a variable to store the slider rectangle
slider_rect = pygame.Rect(150,80,500, 40)

#color
Gray = (192, 192, 192)
dark_gray = (128 ,128 ,128)
white = (255, 255, 255)
black = (0, 0, 0)

#font and text
font = pygame.font.SysFont('munro-small.ttf', 30, True)
font2 =pygame.font.SysFont('munro-small.ttf', 40, True)
sound_text = font.render('Sound:', True, white)
volume_text = font.render(str(background_volume), True, white)
percent = font.render('%', True, white)
setting_text = font2.render('Settings',True,white)
background_text = font2.render('Select Background',True,white)

#background image
background1 =('Background/Classic_background.png')
background2 =('Background/galaxy.png')
background3 =('Background/sea.png')
default_background =('Background/background.png')
# background
selected_bg = None
selected_bg1 = pygame.image.load('Background/Classic_background.png')
selected_bg2 =pygame.image.load('Background/galaxy.png')
selected_bg3 =pygame.image.load('Background/sea.png')
#tray color and ball
selected_tray = None
selected_ball = None
tray_color = pygame.image.load('firstproject/tray.png')
tray_color2 = pygame.image.load('Background/tray2.png')
ball_color = pygame.image.load('firstproject/ball.png')
ball_color2 = pygame.image.load('Background/ball2.png')


background = pygame.image.load(default_background)
# initialize background picture
def display_background(img,scale,x,y):
    image = pygame.image.load(img)
    image = pygame.transform.scale(image,scale)
    screen.blit(image,(x,y))
# buttons for background
button1 = Button('Classic table',170,40,(110,360),6)
button2 = Button('Galaxy table',175,40,(310,360),6)
button3 = Button('Sea table', 170,40,(510,360),6)
#button for back
back_button = Button('Back',100,30,(20,20),6)
#running the loop
running = True
pressed = False
mouse_down = False
#main loop
while running == True:
    mouse_loc = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # check if the button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            if slider_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]!=0:
                mouse_down = True
                # update the volume level based on the mouse position
                background_volume = (mouse_pos[0] - slider_rect.x)/slider_rect.width* 100
                volume = min(max(background_volume,0),100)
                background_volume = int(background_volume)
                volume_text = font.render(str(background_volume), True, white)

        # for background change
    if button1.top_rect.collidepoint(mouse_loc) and pygame.mouse.get_pressed()[0]:
        selected_bg = selected_bg1
        selected_tray = tray_color
        selected_ball = ball_color
        print('classic')
    elif button2.top_rect.collidepoint(mouse_loc) and pygame.mouse.get_pressed()[0]:
        selected_bg = selected_bg2
        selected_tray = tray_color
        selected_ball = ball_color
        print("galaxy")
    elif button3.top_rect.collidepoint(mouse_loc) and pygame.mouse.get_pressed()[0]:
        selected_bg = selected_bg3
        selected_tray = tray_color2
        selected_ball = ball_color2
        print("sea")
    else:
        if back_button.top_rect.collidepoint(mouse_loc) and pygame.mouse.get_pressed()[0]:
            running = False
    pygame.display.update()
    # background of the game itself
    game_background = pygame.image.load(default_background)

    # display background image
    screen.blit(background,(0,0))
    # draw the slider
    pygame.draw.rect(screen, Gray, slider_rect)
    #draw the volume level indicator
    pygame.draw.rect(screen, dark_gray, (slider_rect.x, slider_rect.y, background_volume/100 * slider_rect.width, slider_rect.height))
    # draw the text
    screen.blit(sound_text, (50, 90))
    screen.blit(volume_text,(700,90))
    screen.blit(percent,(725,90))
    screen.blit(setting_text,((800/2)-50,30))
    screen.blit(background_text,((800/2)-125,140))
    # display for change background
    display_background(background1, (150, 150), 120, 200)
    display_background(background2, (150, 150), 320, 200)
    display_background(background3, (150, 150), 520, 200)
    button1.draw_button()
    button2.draw_button()
    button3.draw_button()
    # back to main menu button
    back_button.draw_button()
    if selected_bg:
        pygame.image.save(selected_bg, "selected_bg.png")
        print('selected and imported')
        selected_bg = False
    if selected_tray and selected_ball:
        pygame.image.save(selected_tray,"selected_tray.png")
        pygame.image.save(selected_ball, "selected_ball.png")
    else:
        selected_tray = tray_color
        selected_ball = ball_color

    # save the volume
with open('volume.txt','w') as f:
    f.write(str(background_volume/100))
    #update the screen
    pygame.display.update()

