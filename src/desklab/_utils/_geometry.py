import math


def point_to_segment_distance(point: tuple[int, int], segment_start: tuple[int, int], segment_end: tuple[int, int]) -> float:
    point_x, point_y = point
    start_x, start_y = segment_start
    end_x, end_y = segment_end

    vector_segment_x = end_x - start_x
    vector_segment_y = end_y - start_y

    vector_point_x = point_x - start_x
    vector_point_y = point_y - start_y

    segment_length_squared = vector_segment_x ** 2 + vector_segment_y ** 2

    if segment_length_squared == 0:
        return math.sqrt((point_x - start_x) ** 2 + (point_y - start_y) ** 2)

    dot_product = vector_point_x * vector_segment_x + \
        vector_point_y * vector_segment_y
    projection_ratio = max(0.0, min(1.0, dot_product / segment_length_squared))

    closest_x = start_x + vector_segment_x * projection_ratio
    closest_y = start_y + vector_segment_y * projection_ratio

    distance_x = point_x - closest_x
    distance_y = point_y - closest_y

    return math.sqrt(distance_x ** 2 + distance_y ** 2)


def is_inside_circle(coordinates: tuple[int, int], circle_center: tuple[int, int], circle_radius: int):
    x, y = coordinates
    cx, cy = circle_center
    return (x - cx)**2 + (y - cy)**2 <= circle_radius**2
