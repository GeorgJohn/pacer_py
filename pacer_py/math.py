



def float_to_duration(time: float, unit: str) -> tuple[int, int, int]:
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
