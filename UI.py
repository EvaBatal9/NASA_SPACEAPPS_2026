import pygame
from sys import exit
from Buttons import Button
from zoom_window import Zoom_Window
from pathfinder import find_path
from coord_mapper import find_tile, build_segmented_map, get_tile_image


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
light_blue = (173, 216, 230)

#MAP BASE
base_map = pygame.image.load("Graphics/map.png").convert()
original_width, original_height = base_map.get_size()
base_map = pygame.transform.scale(base_map, (1200, 1000))
segmented_map = build_segmented_map(
    original_width,
    original_height
)

font_big = pygame.font.Font("Minecraft.ttf", 36)
font_small = pygame.font.Font("Minecraft.ttf", 15)

#BUTTONS
green_path = "Graphics/green.PNG"
yellow_path = "Graphics/yellow.PNG"
red_path = "Graphics/red.PNG"
exit_path = "Graphics/exit.PNG"
b_scale = 0.02

green_button = Button(green_path, (20,345+250), b_scale)
yellow_button = Button(yellow_path, (20,345+50+250), b_scale)
red_button = Button(red_path, (20,345+100+250), b_scale)

#SIDEBAR
sidebar = pygame.Rect(0,0,300,1000)
contours = [
    pygame.Rect(0,0,5,800),
    pygame.Rect(295,0,5,800),
    pygame.Rect(0,0,1400,5),
    pygame.Rect(0,795,1400,5),
    pygame.Rect(1395,0,5,800)
]

#BLURB
blurb = """You are a newbie intern for NASA’s 
novel mission, which aims to 
send the very first team of 
human researchers to explore 
Mars. Since your colleagues
have been making fun of you, 
you want to prove your worth 
to them by finding an optimal 
path connecting the landing 
site of the spacecraft to 
the area where the astronauts 
will be taking samples. What 
your colleagues don’t know,
however, is that you have access
to a program that can do it all
for you!

Click anywhere on the map to 
choose your landing zone!
"""

#ZOOM WINDOW
window = Zoom_Window(x=725, y=275)
current_path = []
end_coordinate = (1000, 100)
show_window = False

#EXIT BUTTON
exit_button = Button(exit_path, (320, 25), b_scale)
show_exit = False

selected_tile = None
tile_origin = None


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Detect a click on the map
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            # Check that the click is inside the map area
            if 300 <= mouse_x < 1400 and 0 <= mouse_y < 800:

                # Convert screen coordinates to map coordinates
                x_start = int((mouse_x - 300) * original_width / 1200)
                y_start = int(mouse_y * original_height / 1000)

                start_coordinate = (x_start, y_start)

                print("Starting coordinate:", start_coordinate)

               # Extract the selected tile from the assembled map
                selected_tile, tile_origin = get_tile_image(
                    segmented_map,
                    start_coordinate,
                    original_width,
                    original_height
                )

                print("Selected tile:", selected_tile)
                print("Tile origin:", tile_origin)

                # Calculate path using ORIGINAL map coordinates
                current_path = find_path(
                    start_coordinate,
                    end_coordinate
                )

                window.animation_start = None
                show_window = True
                show_exit = True
                window.animation_start = None
                show_window = True
                show_exit = True
    
    screen.blit(base_map, (300, 0))
    pygame.draw.rect(screen, navy_blue, sidebar)
    pygame.draw.rect(screen, bright_orange, contours[0])
    pygame.draw.rect(screen, bright_orange, contours[1])
    pygame.draw.rect(screen, bright_orange, contours[2])
    pygame.draw.rect(screen, bright_orange, contours[3])
    pygame.draw.rect(screen, bright_orange, contours[4])

    screen.blit(font_big.render("Your Mission", True, white), (40, 30))
    
    y = 90

    for line in blurb.splitlines():
        text_surface = font_small.render(line, True, white)

        x = (300 - text_surface.get_width()) // 2

        screen.blit(text_surface, (x, y))
        y += 20

    green_button.draw(screen)
    screen.blit(font_small.render("Optimal Landing Zone", True, white), (70, 360+250))
    yellow_button.draw(screen)
    screen.blit(font_small.render("Suboptimal Landing Zone", True, white), (70, 360+50+250))
    red_button.draw(screen)
    screen.blit(font_small.render("Dangerous Landing Zone", True, white), (70, 360+100+250))
    
    screen.blit(font_big.render("Legend", True, white), (80, 550)) #went from 300 to 550
    if show_window and show_exit:
        window.draw(screen, current_path, selected_tile, tile_origin)
        exit_button.draw(screen)
        print("tile map",selected_tile)
        print("tile origin",tile_origin)


    if exit_button.is_pressed():
        show_window=False


    pygame.display.flip()


