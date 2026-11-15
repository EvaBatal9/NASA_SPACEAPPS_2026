import pygame
import math

class Zoom_Window:
    thickness = 5
    color = (0, 2, 46)
    contour_color = (255, 80, 50)
    path_color = (255, 0, 0)

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 250, 250)
        self.radius = 325
        self.update_borders()

        self.animation_start = None
        self.animation_duration = 4000 

    def update_borders(self):
        self.center = self.rect.center
        self.inner_radius = self.radius - self.thickness

        self.inner_rect = pygame.Rect(
            self.center[0] - self.inner_radius,
            self.center[1] - self.inner_radius,
            self.inner_radius * 2,
            self.inner_radius * 2
        )

    def draw(self, surface, path=None, map_image=None, tile_origin=None):

        pygame.draw.circle(
            surface,
            self.color,
            self.center,
            self.radius
        )

        if map_image is not None:
            self.draw_path(surface, path, map_image, tile_origin)

        pygame.draw.circle(
            surface,
            self.contour_color,
            self.center,
            self.radius,
            self.thickness
        )
        
    def draw_path(self, surface, path, map_image, tile_origin):

        visible_path = []

        if path is not None and len(path) > 0:

            if self.animation_start is None:
                self.animation_start = pygame.time.get_ticks()

            elapsed = pygame.time.get_ticks() - self.animation_start
            progress = min(elapsed / self.animation_duration, 1)

            visible_points = max(1, int(progress * len(path)))
            visible_path = path[:visible_points]

        tile_width, tile_height = map_image.get_size()
        print("Map image size:", map_image.get_size())
        print("Map image average colour:", pygame.transform.average_color(map_image))
        pygame.image.save(map_image, "debug_tile.png")

        diameter = self.inner_radius * 2
        fit_square = max(diameter / tile_width, diameter / tile_height)*1.03
        fit_diagonal = diameter / math.hypot(tile_width, tile_height)
        scale = fit_square * 0.9 + fit_diagonal * 0.1

        display_width = int(tile_width * scale)
        display_height = int(tile_height * scale)

        zoomed_map = pygame.transform.smoothscale(
            map_image,
            (display_width, display_height)
        )

        temp = pygame.Surface(
            (diameter, diameter),
            pygame.SRCALPHA
        )

        map_x = (diameter - display_width) // 2
        map_y = (diameter - display_height) // 2

        temp.blit(zoomed_map, (map_x, map_y))

        scaled_path = []

        for x, y in visible_path:

            screen_x = map_x + x * scale
            screen_y = map_y + y * scale

            scaled_path.append((int(screen_x), int(screen_y)))
        print("Path points:", len(scaled_path))
        print("First scaled point:", scaled_path[0] if scaled_path else None)
        print("Last scaled point:", scaled_path[-1] if scaled_path else None)

        if len(scaled_path) > 1:
            pygame.draw.lines(
                temp,
                self.path_color,
                False,
                scaled_path,
                500
            )

        mask = pygame.Surface(
            (diameter, diameter),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            mask,
            (255, 255, 255, 255),
            (self.inner_radius, self.inner_radius),
            self.inner_radius
        )

        temp.blit(
            mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        surface.blit(
            temp,
            (
                self.center[0] - self.inner_radius,
                self.center[1] - self.inner_radius
            )
        )
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.update_borders()
