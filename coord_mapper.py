from pathlib import Path
import pygame

tile_folder = Path("Graphics/segmented_map")

# All files in just this folder
file_paths = sorted(
    [str(p) for p in tile_folder.iterdir() if p.is_file()]
)

file_path_grid = []

for i in range(0, len(file_paths), 5):
    rows = file_paths[i:i+5]
    file_path_grid.append(rows)

def find_tile(start, width, height):
    x_start, y_start = start

    length = width / 10
    tile_height = height / 5

    x_tile_index = int(x_start // length)
    y_tile_index = int(y_start // tile_height)

    if not (0 <= x_tile_index < 10 and 0 <= y_tile_index < 5):
        print("Coordinate outside image boundaries!")
        return None

    return file_path_grid[x_tile_index][y_tile_index]

def build_segmented_map(width, height):

    # Create one large surface for all 50 tiles
    segmented_map = pygame.Surface((width, height))

    tile_width = width // 10
    tile_height = height // 5

    # Go through each column
    for x in range(10):

        # Go through each row
        for y in range(5):

            tile_path = file_path_grid[x][y]

            # Load tile
            tile = pygame.image.load(tile_path).convert()

            # Resize tile to fit its grid position
            tile = pygame.transform.scale(
                tile,
                (tile_width, tile_height)
            )

            # Place tile in correct position
            segmented_map.blit(
                tile,
                (x * tile_width, y * tile_height)
            )

    return segmented_map

def get_tile_image(segmented_map, start, width, height):

    x_start, y_start = start

    tile_width = width // 10
    tile_height = height // 5

    x_tile_index = int(x_start // tile_width)
    y_tile_index = int(y_start // tile_height)

    if not (0 <= x_tile_index < 10 and 0 <= y_tile_index < 5):
        print("Coordinate outside image boundaries!")
        return None, None

    # Get top-left corner of selected tile
    tile_x = x_tile_index * tile_width
    tile_y = y_tile_index * tile_height

    # Extract selected tile
    tile_map = segmented_map.subsurface(
        pygame.Rect(tile_x, tile_y, tile_width, tile_height)
    ).copy()

    tile_origin = (tile_x, tile_y)

    return tile_map, tile_origin