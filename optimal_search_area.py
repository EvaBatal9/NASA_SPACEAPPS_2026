
import csv
from pathlib import Path


def read_coordinates(filename):
    points = []
    seen = set()

    filepath = Path(__file__).parent / filename

    with open(filepath, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            longitude = float(row["Longitude"])
            latitude = float(row["Latitude"])

            point = (longitude, latitude)

            if point not in seen:
                points.append(point)
                seen.add(point)

    return points


def to_pixels(points, width, height):
    converted = []

    for longitude, latitude in points:
        x = longitude / 360 * width
        y = (90 - latitude) / 180 * height

        if 0 <= x < width and 0 <= y < height:
            converted.append((x, y))

    return converted


def optimal_search_area(hydrous, aqueous, glacier,
                        start_radius, step, max_radius, min_density):

    points = hydrous + aqueous + glacier
    areas = []

    for center in points:
        x1, y1 = center
        best_radius = 0
        best_diversity = 0
        best_total = 0

        radius = start_radius

        while radius <= max_radius:
            counts = []

            for data in [hydrous, aqueous, glacier]:
                count = 0

                for x2, y2 in data:
                    distance = (x2 - x1)**2 + (y2 - y1)**2

                    if distance <= radius**2:
                        count += 1

                counts.append(count)

            total = sum(counts)

            diversity = 0

            for count in counts:
                if count > 0:
                    diversity += 1

            density = total / (3.14159 * radius**2)

            if diversity >= 2 and density >= min_density:
                best_radius = radius
                best_diversity = diversity
                best_total = total

            radius += step

        if best_radius > 0:
            areas.append((
                center,
                best_radius,
                best_diversity,
                best_total
            ))

    def sorting_key(area):
        return (area[2], area[3])

    areas.sort(key=sorting_key, reverse=True)

    selected = []

    for center, radius, diversity, total in areas:
        x1, y1 = center
        redundant = False

        for other_center, other_radius in selected:
            x2, y2 = other_center

            distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

            if distance < min(radius, other_radius):
                redundant = True
                break

        if not redundant:
            selected.append((center, radius))

    return selected


def convert_grid(center, width, height):
    x, y = center

    square_width = width / 10
    square_height = height / 5

    square_x = int(x // square_width)
    square_y = int(y // square_height)

    local_x = x - square_x * square_width
    local_y = y - square_y * square_height

    return (square_x, square_y), (local_x, local_y)


def get_research_areas(width, height):
    hydrous = to_pixels(
        read_coordinates("hydrous.csv"), width, height
    )

    aqueous = to_pixels(
        read_coordinates("aqueous.csv"), width, height
    )

    glacier = to_pixels(
        read_coordinates("glacier.csv"), width, height
    )

    return optimal_search_area(
        hydrous,
        aqueous,
        glacier,
        50,
        20,
        200,
        0.0001
    )


if __name__ == "__main__":
    areas = get_research_areas(1100, 800)

    for center, radius in areas:
        square, position = convert_grid(center, 1100, 800)

        print("Square:", square)
        print("Local position:", position)
        print("Radius:", radius)
        print()
