



def duration_to_hh_mm_ss(time: float, unit: str) -> tuple[int, int, int]:
    """Convert a float representing time into hours, minutes, and seconds.

    Args:
        time (float): Time in the specified unit.
        unit (str): The unit of the input time ('h', 'min' or 'sec').

    Returns:
        tuple: A tuple containing hours, minutes, and seconds.
    """
    if unit == 'h':
        total_seconds = time * 3600
    elif unit == 'min':
        total_seconds = time * 60
    elif unit == 'sec':
        total_seconds = time
    else:
        raise ValueError("Invalid unit. Please use 'h', 'min', or 'sec'.")
    
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return hours, minutes, seconds


def pace_from_duration_and_distance(duration_sec: int, distance_m: float, target_format: str) -> float:
    """Calculate pace in seconds per meter from duration and distance.

    Args:
        duration_sec (int): Duration in seconds.
        distance_m (float): Distance in meters.
        target_format (str): Target format for pace ('sec/m', 'min/km').

    Returns:
        float: Pace in seconds per meter.
    """
    if distance_m <= 0:
        raise ValueError("Distance must be greater than zero.")
    if target_format == 'min/km':
        return (duration_sec / 60.0) / (distance_m / 1000.0)
    elif target_format == 'sec/m':
        return duration_sec / distance_m
    else:
        raise ValueError(f"Unsupported target format: {target_format}.")
    

def duration_from_pace_and_distance(pace_sec_per_m: float, distance_m: float) -> float:
    """Calculate duration in seconds from pace and distance.

    Args:
        pace_sec_per_m (float): Pace in seconds per meter.
        distance_m (float): Distance in meters.

    Returns:
        float: Duration in seconds.
    """
    if pace_sec_per_m <= 0:
        raise ValueError("Pace must be greater than zero.")
    if distance_m < 0:
        raise ValueError("Distance cannot be negative.")
    return pace_sec_per_m * distance_m


def distance_from_pace_and_duration(pace_sec_per_m: float, duration_sec: float, target_format: str) -> float:
    """Calculate distance in meters from pace and duration.

    Args:
        pace_sec_per_m (float): Pace in seconds per meter.
        duration_sec (float): Duration in seconds.
        target_format (str): Target format for distance ('m', 'km').

    Returns:
        float: Distance in meters.
    """
    if pace_sec_per_m <= 0:
        raise ValueError("Pace must be greater than zero.")
    if duration_sec < 0:
        raise ValueError("Duration cannot be negative.")
    if target_format == 'km':
        return (duration_sec / pace_sec_per_m) / 1000.0
    elif target_format == 'm':
        return duration_sec / pace_sec_per_m
    else:
        raise ValueError(f"Unsupported target format: {target_format}.")