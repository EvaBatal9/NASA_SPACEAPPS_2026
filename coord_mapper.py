from pathlib import Path
import pygame

tile_folder = Path("Graphics/segmented_map")

file_path_grid = [
    [
        str(tile_folder / f"topology{y}x{x}.png")
        for x in range(10)
    ]
    for y in range(5)
]

def find_tile(start, width, height):
    x_start, y_start = start

    length = width / 10
    tile_height = height / 5

    x_tile_index = int(x_start // length)
    y_tile_index = int(y_start // tile_height)

    if not (0 <= x_tile_index < 10 and 0 <= y_tile_index < 5):
        print("Coordinate outside image boundaries!")
        return None

    return file_path_grid[y_tile_index][x_tile_index]

def build_segmented_map(width, height):

    segmented_map = pygame.Surface((width, height))

    tile_width = width // 10
    tile_height = height // 5

    for y in range(5):
        for x in range(10):

            tile_path = file_path_grid[y][x]

            tile = pygame.image.load(tile_path).convert()

            tile = pygame.transform.scale(
                tile,
                (tile_width, tile_height)
            )

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

    print("Start:", start)
    print("Width and height:", width, height)
    print("Tile width:", tile_width)
    print("Tile height:", tile_height)
    print("Tile indices:", x_tile_index, y_tile_index)

    if not (0 <= x_tile_index < 10 and 0 <= y_tile_index < 5):
        print("Coordinate outside image boundaries!")
        return None, None

    tile_x = x_tile_index * tile_width
    tile_y = y_tile_index * tile_height

    tile_map = segmented_map.subsurface(
        pygame.Rect(tile_x, tile_y, tile_width, tile_height)
    ).copy()

    return tile_map, (tile_x, tile_y)

def get_tiles_from_coordinates(coordinates, width, height):

    tiles = []

    for coordinate in coordinates:
        tile = find_tile(coordinate, width, height)

        if tile is not None and tile not in tiles:
            tiles.append(tile)

    return tiles