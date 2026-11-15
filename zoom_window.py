

import pygame

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

        # Inner circular area
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

        if path is not None and map_image is not None:
            self.draw_path(surface, path, map_image, tile_origin)

        pygame.draw.circle(
            surface,
            self.contour_color,
            self.center,
            self.radius,
            self.thickness
        )
            
        
    def draw_path(self, surface, path, map_image, tile_origin):

        if len(path) == 0:
            return

        if self.animation_start is None:
            self.animation_start = pygame.time.get_ticks()

        elapsed = pygame.time.get_ticks() - self.animation_start
        progress = min(elapsed / self.animation_duration, 1)

        visible_points = max(1, int(progress * len(path)))
        visible_path = path[:visible_points]

        # Get dimensions of selected tile
        tile_width, tile_height = map_image.get_size()

        # Fit the entire tile inside the circular window
        diameter = self.inner_radius * 2

        scale = min(
            diameter / tile_width,
            diameter / tile_height
        )

        display_width = int(tile_width * scale)
        display_height = int(tile_height * scale)

        zoomed_map = pygame.transform.smoothscale(
            map_image,
            (display_width, display_height)
        )

        # Position tile in the centre of the circle
        map_x = self.center[0] - display_width // 2
        map_y = self.center[1] - display_height // 2

        # Temporary surface
        temp = pygame.Surface(
            surface.get_size(),
            pygame.SRCALPHA
        )

        # Draw the actual selected tile
        temp.blit(zoomed_map, (map_x, map_y))

        # Convert global map coordinates into tile coordinates
        tile_origin_x, tile_origin_y = tile_origin

        scaled_path = []

        for x, y in visible_path:

            local_x = x - tile_origin_x
            local_y = y - tile_origin_y

            screen_x = map_x + local_x * scale
            screen_y = map_y + local_y * scale

            scaled_path.append((int(screen_x), int(screen_y)))

        # Draw path
        if len(scaled_path) > 1:
            pygame.draw.lines(
                temp,
                self.path_color,
                False,
                scaled_path,
                2
            )

        # Draw start marker only if start is inside selected tile
        start_x, start_y = path[0]

        if (0 <= start_x - tile_origin_x < tile_width and
            0 <= start_y - tile_origin_y < tile_height):

            pygame.draw.circle(
                temp,
                (173, 216, 230),
                scaled_path[0],
                7
            )

        # Draw endpoint marker only if endpoint is inside selected tile
        end_x, end_y = path[-1]

        if (0 <= end_x - tile_origin_x < tile_width and
            0 <= end_y - tile_origin_y < tile_height):

            x, y = scaled_path[-1]

            pygame.draw.line(
                temp,
                (173, 216, 230),
                (x - 7, y - 7),
                (x + 7, y + 7),
                3
            )

            pygame.draw.line(
                temp,
                (173, 216, 230),
                (x - 7, y + 7),
                (x + 7, y - 7),
                3
            )

        # Circular clipping mask
        mask = pygame.Surface(
            surface.get_size(),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            mask,
            (255, 255, 255, 255),
            self.center,
            self.inner_radius
        )

        temp.blit(
            mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        surface.blit(temp, (0, 0))


    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.update_borders()
