import pygame
from maingame import Button

pygame.init()
white = (255,255,255)
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('HELP')
bg = pygame.image.load('Background/background.png')

def text_display(text,x,y,style):

    render_text = style.render(text,True,white)
    screen.blit(render_text,(x,y))

#text
titlefont = pygame.font.Font('munro-small.ttf',40)
header = pygame.font.Font('munro-small.ttf',35)
textfont = pygame.font.Font('munro-small.ttf',25)
back = Button('Back', 100,30,(20,20),6)

pressed = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if back.pressed:
            setattr(back, "pressed", False)
            running = False
        pygame.display.update()

    screen.blit(bg,(0,0))
    text_display('HELP',370,0,titlefont)
    text_display('Keyboard Keys',20,50,header)
    text_display('Keys',600,50,header)
    text_display('2 Player',50,75,header)
    text_display('1. Player 1 control',20,120,textfont)
    text_display('w - going up',580,120,textfont)
    text_display('s - going down', 580, 150, textfont)
    text_display('2. Player 2 control', 20, 180, textfont)
    text_display('up arrow - going up', 497, 180, textfont)
    text_display('down arrow - going down', 470, 210, textfont)
    text_display('3. Serve Ball(Player1)',20,250,textfont)
    text_display('4. Serve Ball(Player2)', 20, 300,textfont)
    text_display('Left Shift',580,250,textfont)
    text_display('Right Shift', 580, 300, textfont)
    text_display('5. Pause game', 20, 350, textfont)
    text_display('Space Bar', 580, 350, textfont)
    #draw back button
    back.draw_button()

    pygame.display.update()