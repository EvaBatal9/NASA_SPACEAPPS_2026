import pygame
from sys import exit
from Buttons import Button
from zoom_window import Zoom_Window
from pathfinder import path

pygame.init()
screen = pygame.display.set_mode((1400, 800))

#COLOURS
background_colour = (0,0,0)
brown = (75, 46, 42)
beige = (255, 208, 163)
bright_orange = (255, 80, 50)
white = (246, 241, 234)
yellow = (253, 185, 21)
navy_blue = (0, 2, 46)

#MAP BASE
base_map = pygame.image.load("Graphics/base_map.png").convert()
base_map = pygame.transform.scale(base_map, (1200, 1000))

#FONTS
font_big = pygame.font.Font("Minecraft.ttf", 36)
font_small = pygame.font.Font("Minecraft.ttf", 20)

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

#SIDEBAR
sidebar = pygame.Rect(0,0,300,1000)
contours = [
    pygame.Rect(0,0,5,800),
    pygame.Rect(295,0,5,800),
    pygame.Rect(0,0,1400,5),
    pygame.Rect(0,795,1400,5),
    pygame.Rect(1395,0,5,800)
]

#ZOOM WINDOW
window = Zoom_Window(x=725, y=275)

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


    screen.blit(base_map, (300, 0))
    pygame.draw.rect(screen, navy_blue, sidebar)
    pygame.draw.rect(screen, bright_orange, contours[0])
    pygame.draw.rect(screen, bright_orange, contours[1])
    pygame.draw.rect(screen, bright_orange, contours[2])
    pygame.draw.rect(screen, bright_orange, contours[3])
    pygame.draw.rect(screen, bright_orange, contours[4])

    screen.blit(font_big.render("Mission Type", True, white), (40, 30))
    button_MT_1.draw(screen)
    screen.blit(font_small.render("Mission Criteria 1", True, white), (70, 110))
    button_MT_2.draw(screen)
    screen.blit(font_small.render("Mission Criteria 2", True, white), (70, 160))
    button_MT_3.draw(screen)
    screen.blit(font_small.render("Mission Criteria 3", True, white), (70, 210))
    button_MT_4.draw(screen)
    screen.blit(font_small.render("Mission Criteria 4", True, white), (70, 260))

    

    window.draw(screen, path)


    pygame.display.flip()

   

pygame.quit()