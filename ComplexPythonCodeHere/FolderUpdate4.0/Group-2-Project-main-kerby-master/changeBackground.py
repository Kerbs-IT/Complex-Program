import pygame,sys
from pygame import mixer
from maingame import Button
pygame.init()
screen = pygame.display.set_mode((800,600))
table_button = False
run = True
#def change_background():
background1 =('Background/Classic_background.png')
background2 =('Background/galaxy.png')
background3 =('Background/sea.png')
default_background =('Background/background.png')
background = pygame.image.load(default_background)
font = pygame.font.Font('munro-small.ttf', 30)
clicksound = mixer.Sound("button_click.wav")
clicksound.set_volume(0.08)
def display_background(img,scale,x,y):
    image = pygame.image.load(img)
    image = pygame.transform.scale(image,scale)
    screen.blit(image,(x,y))

#button
descrip1 = Button('Classic Table',200,40,(100,285),6)
descrip2 = Button('Galaxy Table',200,40,(500,285),6)
descrip3 = Button('Sea Table',200,40,(300,535),6)

while run:
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if descrip1.pressed:
            table_button = True
        else:
            if table_button == True:
                table_button=False

    screen.blit(background,(0,0))
    display_background(background1,(200,200),100,80)
    display_background(background2, (200, 200), 500, 80)
    display_background(background3, (200, 200),300,330)
    descrip1.draw_button()
    descrip2.draw_button()
    descrip3.draw_button()
    pygame.display.update()
