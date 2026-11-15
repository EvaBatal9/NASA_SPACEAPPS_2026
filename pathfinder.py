from __future__ import annotations
import math
from typing import Any
from PIL import Image
import heapq

def draw_path(image_path, path, output_path="shortest_path.png"):

    # Open original image
    image = Image.open(image_path).convert("RGB")

    # Colour every pixel in the path red
    for x, y in path:
        image.putpixel((x, y), (255, 0, 0))

    # Save the resulting image
    image.save(output_path)

    print("Image saved as:", output_path)


def load_grid(image_path):
    image = Image.open(image_path).convert("L")

    width, height = image.size

    grid = []

    for y in range(height):
        row = []
        for x in range(width):

            pixel = image.getpixel((x, y))

            # White = walkable, black = wall
            if pixel >150:
                row.append(255)
            else:
                row.append(0)

        grid.append(row)

    return grid

class Vertex:
    item: Any
    neighbours: set[tuple[Vertex, int]]
    def __init__(self, item, neighbours):
        self.item = item
        self.neighbours = neighbours

class Graph:
    vertices: dict
    def build_grid(self, grid):
        height = len(grid)
        width = len(grid[0])

        # Create a vertex for every white pixel
        for y in range(height):
            for x in range(width):
                if grid[y][x] == 255:
                    self.add_vertex((x, y))

        # Connect neighbouring white pixels
        directions = [
            (0, 1),    # Down
            (0, -1),   # Up
            (1, 0),    # Right
            (-1, 0),   # Left
            (1, 1),    # Down-right
            (1, -1),   # Up-right
            (-1, 1),   # Down-left
            (-1, -1)   # Up-left
        ]

        for y in range(height):
            for x in range(width):

                if grid[y][x] != 255:
                    continue

                for dx, dy in directions:
                    nx = x + dx
                    ny = y + dy

                    # Check that neighbour is inside grid
                    if 0 <= nx < width and 0 <= ny < height:

                        # Check that neighbour is walkable
                        if grid[ny][nx] == 255:
                            if dx != 0 and dy != 0:
                                weight = math.sqrt(2)
                            else:
                                weight = 1

                            self.add_edge((x, y), (nx, ny), weight)
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, item):
        self.vertices[item] = Vertex(item, set())

    def add_edge(self, item1, item2, weight):
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            # Add v1 and v2 to each other neighbours attribute
            v1.neighbours.add((v2, weight))
            v2.neighbours.add((v1, weight))

    def dijkstra(self, start, end):

        if start not in self.vertices or end not in self.vertices:
            return "Invalid start or end coordinate!"

        distances = {start: 0}
        previous = {}

        # Priority queue: (distance, coordinate)
        queue = [(0, start)]

        while queue:

            curr_distance, curr_vertex = heapq.heappop(queue)

            # Ignore outdated queue entries
            if curr_distance > distances[curr_vertex]:
                continue

            # We reached the destination
            if curr_vertex == end:
                break

            vertex = self.vertices[curr_vertex]

            for neighbour, weight in vertex.neighbours:

                new_distance = curr_distance + weight

                if new_distance < distances.get(neighbour.item, math.inf):

                    distances[neighbour.item] = new_distance
                    previous[neighbour.item] = curr_vertex

                    heapq.heappush(
                        queue,
                        (new_distance, neighbour.item)
                    )

        # Check if a path exists
        if end not in distances:
            return "No path!"

        # Reconstruct the path
        path = []
        curr = end

        while curr != start:
            path.append(curr)
            curr = previous[curr]

        path.append(start)
        path.reverse()

        return distances[end], path

    def dijkstra_min(self, unvisited, distances):
        # Find vertex from unvisited with the lowest distance from origin
        smallest = math.inf
        vertex = None
        for v in unvisited:
            if distances[v][0] < smallest:
                vertex = v
                smallest = distances[v][0]
        return vertex

    def dijkstra_path(self, start, end, distances):
        # Return backlog path
        curr = end
        path = [end]
        while curr != start:
            path.insert(0, distances[curr][1])
            curr = distances[curr][1]
        return path
    

# Load your image
grid = load_grid("Graphics/map.png")

# Create graph
graph = Graph()
graph.build_grid(grid)

# Define starting and ending coordinates
x_start, y_start = 200, 300
x_end, y_end = 1500, 100

# Find shortest path
result = graph.dijkstra(
    (x_start, y_start),
    (x_end, y_end)
)

if isinstance(result, tuple):
    distance, path = result

    print("Shortest distance:", distance)
    print("Shortest path:", path)
    draw_path("Graphics/map.png", path, "shortest_path.png" )

else:
    print(result)

print(len(path))