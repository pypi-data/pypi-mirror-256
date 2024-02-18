from __future__ import annotations

from typing import List, Union

import numpy as np
import pyproj
from shapely.geometry import LineString, Point, Polygon


def gml_point_to_shapely(gml_point_coordinates: str) -> Point:
    """
    Converts a GML point coordinate string to a Shapely Point object.

    Args:
        gml_point_coordinates (str): The GML point coordinate string in the format "(x,y)".

    Returns:
        (Shapely.Point): The Shapely Point object.

    """
    coordinates = [float(x) for x in gml_point_coordinates.replace("(", "").replace(")", "").replace("'", "").replace(" ", "").split(",")]
    return Point(coordinates)


def shapely_point_to_gml(shapely_point: Point):
    """
    Converts a Shapely Point object to a GML point coordinate string.

    Args:
        shapely_point (Point): The Shapely point".

    Returns:
        (str): gml:point string representation.

    """
    if shapely_point.has_z:
        return f"{round(shapely_point.x, 3)},{round(shapely_point.y, 3)},{round(shapely_point.z, 3)}"
    else:
        return f"{round(shapely_point.x, 3)},{round(shapely_point.y, 3)}"


def gml_linestring_to_shapely(gml_linestring_coordinates: str) -> LineString:
    """
    Converts a GML linestring coordinate string to a Shapely LineString object.

    Args:
        gml_linestring_coordinates (str): A string of GML linestring coordinates in "x,y" format separated by spaces.

    Returns:
        (Shapely.LineString): A Shapely LineString object.

    """
    return LineString([tuple(map(float, x.split(","))) for x in gml_linestring_coordinates.split(" ")])


def gml_polygon_to_shapely(gml_linestring_coordinates: str) -> Polygon:
    """
    Converts a GML polygon to a Shapely Polygon object.

    Args:
        gml_linestring_coordinates (str): A string containing the GML coordinates of the polygon.

    Returns:
        (Polygon): A Shapely Polygon object.

    """
    return Polygon([tuple(map(float, x.split(","))) for x in gml_linestring_coordinates.split(" ")])


class ShapelyTransform:
    """A utility class to transform between RD and WGS84 coordinate systems."""

    rd = pyproj.CRS("EPSG:28992")
    wgs = pyproj.CRS("EPSG:4326")
    transformer_to_wgs = pyproj.Transformer.from_crs(rd, wgs)
    transformer_to_rd = pyproj.Transformer.from_crs(wgs, rd)

    @classmethod
    def rd_to_wgs(cls, shapely: Union[Point, LineString, Polygon]) -> Union[Point, LineString, Polygon]:
        """
        Convert a Shapely geometry from Dutch RD (Rijksdriehoekstelsel) coordinates (EPSG:28992) to WGS84 coordinates (EPSG:4326).

        Args:
            shapely (Union[Point, LineString, Polygon]): A Shapely geometry in Dutch RD coordinates.

        Returns:
            (Union[Point, LineString, Polygon]): A Shapely geometry in WGS84 coordinates.

        """
        return cls._convert(shapely, cls.transformer_to_wgs)

    @staticmethod
    def _convert(shapely: Union[Point, LineString, Polygon], transformer: pyproj.Transformer) -> Union[Point, LineString, Polygon]:
        if isinstance(shapely, Point):
            return Point(*reversed(transformer.transform(shapely.x, shapely.y)))

        elif isinstance(shapely, LineString):
            return LineString(zip(*reversed(transformer.transform(*shapely.coords.xy))))

        elif isinstance(shapely, Polygon):
            return LineString(zip(*reversed(transformer.transform(*shapely.exterior.coords.xy))))
        else:
            return shapely


def reverse_line(shapely_polyline: LineString) -> LineString:
    """
    Reverses the order of coordinates in a Shapely LineString object.

    Args:
        shapely_polyline (LineString): The LineString object to reverse.

    Returns:
        (LineString): A new LineString object with the coordinates in reverse order.

    """
    return LineString(list(shapely_polyline.coords)[::-1])


def get_azimuth_from_points(point1: Point, point2: Point) -> float:
    """
    Calculates the azimuth angle between two points.

    Args:
        point1 (Point): The first Point object.
        point2 (Point): The second Point object.

    Returns:
        (float): The azimuth angle in degrees.

    """
    angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
    return float(np.degrees(angle)) if angle >= 0 else float(np.degrees(angle) + 360)


def check_point_in_area(point_str: str, area: Polygon):
    point_to_test = Point([float(item) for item in point_str.split(",")])
    return point_to_test.within(area)


def cut(line: LineString, distance: float) -> List[LineString]:
    # todo: if 0 then its not working... sho
    if distance == 0:
        return [line]

    # todo: move to shapley helpers
    # Cuts a 3d line in two at a distance from its starting point
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coordinates = list(line.coords)
    for i, p in enumerate(coordinates):
        pd = line.project(Point(p))
        if pd == distance:
            return [LineString(coordinates[: i + 1]), LineString(coordinates[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            # todo: check if z present, if not switch and do not use z
            return [LineString(coordinates[:i] + [(cp.x, cp.y, cp.z)]), LineString([(cp.x, cp.y, cp.z)] + coordinates[i:])]


def cut_profile(line: LineString, measure_from: float, measure_to: float) -> LineString:
    if measure_from > measure_to:
        measure_from, measure_to = measure_to, measure_from
    if measure_from == 0:
        new_line = line
    else:
        new_line = cut(line, measure_from)[1]

    point = line.interpolate(measure_to)
    new_measure = new_line.project(point)
    result = cut(new_line, new_measure)[0]
    return result


def offset_linestring(line: LineString, distance: float, direction: str) -> LineString:
    # Extract coordinates from LineString
    coords = np.array(line.coords)

    # Calculate direction vector
    direction_vector = np.array([coords[-1][0] - coords[0][0], coords[-1][1] - coords[0][1]])
    direction_vector = direction_vector / np.linalg.norm(direction_vector)

    # Calculate perpendicular vector
    if direction == "up":
        perpendicular_vector = np.array([-direction_vector[1], direction_vector[0]])  # Rotate by 90 degrees clockwise
    elif direction == "down":
        perpendicular_vector = np.array([direction_vector[1], -direction_vector[0]])  # Rotate by 90 degrees counterclockwise
    else:
        raise ValueError("Direction must be 'up' or 'down'.")

    offset_coords = []
    for coord in coords:
        new_coord = coord + distance * perpendicular_vector
        offset_coords.append((new_coord[0], new_coord[1]))

    return LineString(offset_coords)


# def shared_segments(line1: LineString, line2: LineString) -> Tuple[LineString, LineString]:
#     segments1 = [LineString((line1.coords[i], line1.coords[i + 1])) for i in range(len(line1.coords) - 1)]
#     segments2 = [LineString((line2.coords[i], line2.coords[i + 1])) for i in range(len(line2.coords) - 1)]
#
#     shared1 = [_ for _ in segments1 if _.intersects(line2)]
#     shared2 = [_ for _ in segments2 if _.intersects(line1)]
#
#     if len(shared1) != 1 or len(shared2) != 1:
#         raise ValueError("None, or more shared")
#
#     return shared1[0], shared2[0]
#
#
# def get_farthest_points(line1: LineString, line2: LineString) -> Tuple[Tuple[float, float], Tuple[float, float]]:
#     # Find the point on line1 farthest from line2
#     farthest_point_line1 = max(line1.coords, key=lambda p: line2.distance(Point(p[0], p[1])))
#
#     # Find the point on line2 farthest from line1
#     farthest_point_line2 = max(line2.coords, key=lambda p: line1.distance(Point(p[0], p[1])))
#
#     return farthest_point_line1, farthest_point_line2
