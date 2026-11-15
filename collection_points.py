from optimal_search_area import optimal_search_area
from coord_mapper import build_segmented_map, get_tiles_from_coordinates

coordinates = [
    (510, 49),
    (734, 93),
    (300, 450),
    (900, 600)
]

start_coordinate = [(100,200)]

tiles = get_tiles_from_coordinates(coordinates, 1000, 800)
print(tiles)
for t in tiles:
    if t != get_tiles_from_coordinates(start_coordinate, 1000, 800):
        tiles.remove(t)
print(tiles)