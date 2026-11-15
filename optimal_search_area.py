def optimal_search_area(hydrous, aqueous, glacier,
                   start_radius, step, max_radius, min_density):

    points = hydrous + aqueous + glacier
    areas = []

    for center in points:
        x1, y1 = center
        best_radius = 0
        radius = start_radius

        while radius <= max_radius:
            counts = []

            for data in [hydrous, aqueous, glacier]:
                count = 0

                for x2, y2 in data:
                    distance = (x2-x1)**2 + (y2-y1)**2

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
            
            radius += step

        if best_radius > 0:
            areas.append((center, best_radius))

    selected = []

    for center, radius in areas:
        x1, y1 = center
        redundant = False

        for other_center, other_radius in selected:
            x2, y2 = other_center

            distance = ((x2-x1)**2 + (y2-y1)**2)**0.5

            if distance < min(radius, other_radius):
                redundant = True
                break

        if not redundant:
            selected.append((center, radius))

    return selected


def convert_grid(center):

    x, y = center

    square_x = x // 100 
    square_y = y // 100 

    local_x = x % 100
    local_y = y % 100

    return (square_x, square_y), (local_x, local_y)