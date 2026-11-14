import pygame
from sys import exit

pygame.init()
window = pygame.display.set_mode((800, 500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()