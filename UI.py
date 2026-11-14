import pygame
from sys import exit
from Buttons import Button

pygame.init()
screen = pygame.display.set_mode((1200, 800))

#COLOURS
background_colour = (0,0,0)
brown = (75, 46, 42)
beige = (255, 208, 163)
bright_orange = (255, 154, 77)
white = (246, 241, 234)

#FONTS
font = pygame.font.Font("Minecraft.ttf", 36)

#BUTTONS
button_on_path = "Graphics/button_on.PNG"
button_off_path = "Graphics/button_off.PNG"
b_scale = 0.02

button_MT_1 = Button(button_off_path, (20,100), b_scale)
button_MT_2 = Button(button_off_path, (20,150), b_scale)
button_MT_3 = Button(button_off_path, (20,200), b_scale)
button_MT_4 = Button(button_off_path, (20,250), b_scale)

#BUTTON STATES
button_MT_1_on = False
button_MT_2_on = False
button_MT_3_on = False
button_MT_4_on = False


sidebar = pygame.Rect(0,0,300,1000)
contours = [
    pygame.Rect(0,0,10,800),
    pygame.Rect(290,0,10,800),
    pygame.Rect(0,0,300,10),
    pygame.Rect(0,790,300,10)
]

while True:
   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    #IF STATEMENT FOR MISSION CRITERIA 1
    if button_MT_1.is_pressed():
        button_MT_1_on = not button_MT_1_on

        if button_MT_1_on:
            button_MT_1.change_image(button_on_path)
        else:
            button_MT_1.change_image(button_off_path)

    #IF STATEMENT FOR MISSION CRITERIA 2
    if button_MT_2.is_pressed():
        button_MT_2_on = not button_MT_2_on

        if button_MT_2_on:
            button_MT_2.change_image(button_on_path)
        else:
            button_MT_2.change_image(button_off_path)
    
    #IF STATEMENT FOR MISSION CRITERIA 3
    if button_MT_3.is_pressed():
        button_MT_3_on = not button_MT_3_on

        if button_MT_3_on:
            button_MT_3.change_image(button_on_path)
        else:
            button_MT_3.change_image(button_off_path)

    #IF STATEMENT FOR MISSION CRITERIA 4
    if button_MT_4.is_pressed():
        button_MT_4_on = not button_MT_4_on

        if button_MT_4_on:
            button_MT_4.change_image(button_on_path)
        else:
            button_MT_4.change_image(button_off_path)





    
    screen.fill(background_colour)
    pygame.draw.rect(screen, beige, sidebar)
    pygame.draw.rect(screen, bright_orange, contours[0])
    pygame.draw.rect(screen, bright_orange, contours[1])
    pygame.draw.rect(screen, bright_orange, contours[2])
    pygame.draw.rect(screen, bright_orange, contours[3])

    screen.blit(font.render("Mission Type", True, brown), (40, 30))
    button_MT_1.draw(screen)
    button_MT_2.draw(screen)
    button_MT_3.draw(screen)
    button_MT_4.draw(screen)



    pygame.display.flip()

   

pygame.quit()