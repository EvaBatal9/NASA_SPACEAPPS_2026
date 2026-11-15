import pygame
from pathfinder import path
import numpy as np

path = np.array(path)

min_x = np.min(path[:, 0])
max_x = np.max(path[:, 0])

min_y = np.min(path[:, 1])
max_y = np.max(path[:, 1])


width = max_x - min_x
height = max_y - min_y

RECT_SIZE = 250


scale = min(
    RECT_SIZE / width,
    RECT_SIZE / height
)


scaled_path = (path - [min_x, min_y]) * scale


offset_x = (RECT_SIZE - width * scale) / 2
offset_y = (RECT_SIZE - height * scale) / 2

scaled_path += [offset_x, offset_y]


scaled_path = scaled_path.astype(int)