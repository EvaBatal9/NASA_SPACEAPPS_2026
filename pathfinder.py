
import math
import heapq
from PIL import Image


def load_grid(image_path):
    image = Image.open(image_path).convert("L")

    width, height = image.size
    grid = []

    for y in range(height):
        row = []

        for x in range(width):
            pixel = image.getpixel((x, y))

            # White = walkable, black = wall
            if pixel<150:
                row.append(255)
            else:
                row.append(0)

        grid.append(row)

    return grid


def draw_path(image_path, path, output_path="shortest_path.png"):
    image = Image.open(image_path).convert("RGB")

    for x, y in path:
        if 0 <= x < image.width and 0 <= y < image.height:
            image.putpixel((x, y), (255, 0, 0))

    image.save(output_path)
    print("Image saved as:", output_path)


def dijkstra_grid(grid, start, targets):
    height = len(grid)
    width = len(grid[0])

    x, y = start

    if not (0 <= x < width and 0 <= y < height):
        return None

    if grid[y][x] != 255:
        return None

    distances = {start: 0}
    previous = {}
    queue = [(0, start)]

    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]

    while queue:
        distance, current = heapq.heappop(queue)

        if distance > distances[current]:
            continue

        if current in targets:
            path = []
            point = current

            while point != start:
                path.append(point)
                point = previous[point]

            path.append(start)
            path.reverse()

            return distance, path, current

        x, y = current

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if grid[ny][nx] != 255:
                continue

            if dx != 0 and dy != 0:
                if grid[y][nx] != 255:
                    continue

                if grid[ny][x] != 255:
                    continue

                weight = math.sqrt(2)
            else:
                weight = 1

            neighbour = (nx, ny)
            new_distance = distance + weight

            if new_distance < distances.get(neighbour, math.inf):
                distances[neighbour] = new_distance
                previous[neighbour] = current

                heapq.heappush(
                    queue, (new_distance, neighbour)
                )

    return None


def find_path(image_path, start, end):
    grid = load_grid(image_path)

    result = dijkstra_grid(grid, start, {end})

    if result is None:
        return []

    distance, path, destination = result
    return path


def path_to_research_area(image_path, start, areas):
    grid = load_grid(image_path)

    height = len(grid)
    width = len(grid[0])

    targets = {}

    for center, radius in areas:
        cx, cy = center

        min_x = max(0, int(cx - radius))
        max_x = min(width - 1, math.ceil(cx + radius))

        min_y = max(0, int(cy - radius))
        max_y = min(height - 1, math.ceil(cy + radius))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):

                if grid[y][x] != 255:
                    continue

                distance_squared = (x - cx)**2 + (y - cy)**2

                if distance_squared <= radius**2:
                    if (x, y) not in targets:
                        targets[(x, y)] = (center, radius)

    if not targets:
        return None, math.inf, None

    result = dijkstra_grid(grid, start, targets)

    if result is None:
        return None, math.inf, None

    distance, path, destination = result
    area = targets[destination]

    return area, distance, path
           
            v1.neighbours.add((v2, weight))
            v2.neighbours.add((v1, weight))

def dijkstra(self, start, end):

        if start not in self.vertices or end not in self.vertices:
            return "Invalid start or end coordinate!"

        distances = {start: 0}
        previous = {}

       
        queue = [(0, start)]

        while queue:

            curr_distance, curr_vertex = heapq.heappop(queue)

           
            if curr_distance > distances[curr_vertex]:
                continue

         
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

        
        if end not in distances:
            return "No path!"

       
        path = []
        curr = end

        while curr != start:
            path.append(curr)
            curr = previous[curr]

        path.append(start)
        path.reverse()

        return distances[end], path

    def dijkstra_min(self, unvisited, distances):
        
        smallest = math.inf
        vertex = None
        for v in unvisited:
            if distances[v][0] < smallest:
                vertex = v
                smallest = distances[v][0]
        return vertex

    def dijkstra_path(self, start, end, distances):
       
        curr = end
        path = [end]
        while curr != start:
            path.insert(0, distances[curr][1])
            curr = distances[curr][1]
        return path
    
def find_path(image_path, start, end):

   
    grid = load_grid(image_path)

    
    graph = Graph()
    graph.build_grid(grid)

    
    result = graph.dijkstra(start, end)

    if isinstance(result, tuple):
        print("found path")
        distance, path = result
        return path
    return []
