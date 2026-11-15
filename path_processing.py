import pygame
from pathfinder import path
import numpy as np

path = np.array(path)

# Find boundaries of the path
min_x = np.min(path[:, 0])
max_x = np.max(path[:, 0])

min_y = np.min(path[:, 1])
max_y = np.max(path[:, 1])

# Calculate dimensions
width = max_x - min_x
height = max_y - min_y

RECT_SIZE = 250

# Calculate scaling factor
scale = min(
    RECT_SIZE / width,
    RECT_SIZE / height
)

# Scale coordinates and reposition them
scaled_path = (path - [min_x, min_y]) * scale

# Center the path inside the 250x250 rectangle
offset_x = (RECT_SIZE - width * scale) / 2
offset_y = (RECT_SIZE - height * scale) / 2

scaled_path += [offset_x, offset_y]

# Convert to integers for Pygame
scaled_path = scaled_path.astype(int)