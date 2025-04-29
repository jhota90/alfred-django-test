import math
from datetime import timedelta


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points (latitude/longitude) using the Haversine formula.
    Result in kilometers (km).
    """
    R = 6371  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def calculate_estimated_arrival_time(distance_km) -> timedelta:
    """
    Calculates an estimated time of arrival based on an average speed.
    """
    avg_speed_kmph = 40  # velocidad promedio asumida (puedes ajustar)
    hours = distance_km / avg_speed_kmph
    return timedelta(hours=hours)
