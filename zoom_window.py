

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

    def draw(self, surface, path=None):

        # Draw circular background
        pygame.draw.circle(
            surface,
            self.color,
            self.center,
            self.radius
        )

        # Draw path if provided
        if path is not None:
            self.draw_path(surface, path)

        # Draw circular contour
        pygame.draw.circle(
            surface,
            self.contour_color,
            self.center,
            self.radius,
            self.thickness
        )

    def draw_path(self, surface, path):

        if len(path) == 0:
            return

        # Find path boundaries
        min_x = min(p[0] for p in path)
        max_x = max(p[0] for p in path)

        min_y = min(p[1] for p in path)
        max_y = max(p[1] for p in path)

        width = max_x - min_x
        height = max_y - min_y

        padding = 50

        # Available space after preserving constant padding
        available_radius = self.inner_radius - padding

        available_width = available_radius * 2
        available_height = available_radius * 2

        # Calculate proportional scaling
        scale = min(
            available_width / max(width, 1),
            available_height / max(height, 1)
        )

        # Center path inside circle
        offset_x = self.center[0] - width * scale / 2
        offset_y = self.center[1] - height * scale / 2
        scaled_path = []

        for x, y in path:
            new_x = offset_x + (x - min_x) * scale
            new_y = offset_y + (y - min_y) * scale

            scaled_path.append((int(new_x), int(new_y)))

        # Clip path to circular area
        old_clip = surface.get_clip()

        # Create circular clipping mask
        mask = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(
            mask,
            (255, 255, 255, 255),
            self.center,
            self.inner_radius
        )

        # Draw path onto transparent temporary surface
        temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        if len(scaled_path) > 1:
            pygame.draw.lines(
                temp,
                self.path_color,
                False,
                scaled_path,
                2
            )
        else:
            pygame.draw.circle(
                temp,
                self.path_color,
                scaled_path[0],
                2
            )

        x_size = 7
        x_color = (255, 255, 255)
        x_thickness = 3

        start = scaled_path[0]
        end = scaled_path[-1]

        # Filled circle for START
        pygame.draw.circle(
            temp,
            (255, 255, 255),
            start,
            7
        )

        # X for END
        x_size = 7
        x_thickness = 3

        x, y = end

        pygame.draw.line(
            temp, (255, 255, 255),
            (x - x_size, y - x_size),
            (x + x_size, y + x_size),
            x_thickness
        )

        pygame.draw.line(
            temp, (255, 255, 255),
            (x - x_size, y + x_size),
            (x + x_size, y - x_size),
            x_thickness
        )

        temp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        surface.blit(temp, (0, 0))

        surface.set_clip(old_clip)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.update_borders()
