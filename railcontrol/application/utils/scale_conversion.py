def mm_to_scale_miles(mm: int, scale:int = 148) -> float:
    MILES_MM = 1_609_344  # mm in a scale mile
    return (mm * scale) / MILES_MM

def travel_time_seconds(mm: int, mph: float, scale: int = 148) -> float:
    return (mm_to_scale_miles(mm, scale) / mph) * 3600