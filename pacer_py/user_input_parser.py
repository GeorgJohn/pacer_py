import re


def parse_option(opt_str: str, opt: dict[int, str]) -> int:
    """Parse an option string into the corresponding option ID.

    Args:
        opt_str (str): The option string provided by the user.
        opt (dict[int, str]): A dictionary mapping option IDs to their descriptions.

    Returns:
        int: The ID of the selected option.

    Raises:
        ValueError: If the input is not a valid option.
    """
    if opt_str.isdigit():
        opt_number = int(opt_str)
        if opt_number in opt.keys():
            return opt_number
        else:
            raise ValueError(f"Chosen option {opt_number} is not available!")
    else:
        raise ValueError(f"Input '{opt_str}' is not a valid number!")


def parse_duration(duration_str: str) -> int:
    """Parse a duration string into total seconds.

    Args:
        duration_str (str): Duration string in the format 'HH:MM:SS', 'MM:SS', or 'SS'.

    Returns:
        int: Total duration in seconds.

    """
    # Check if string contains any letter
    duration_str_split = duration_str.split(':')

    if len(duration_str_split) > 3:
        raise ValueError(f"Given duration contains too many fields ({len(duration_str_split)}). Please use format: 'HH:MM:SS'")

    for str_split in duration_str_split:
        if not re.match("^[0-9]*$", str_split):
            raise ValueError(f"Given duration '{duration_str}' can't be parse to a duration! Please use format: 'HH:MM:SS'")

    duration_split = [int(e) for e in duration_str_split]

    hours, minutes, seconds = 0, 0, 0
    if len(duration_split) >= 3:
        hours, minutes, seconds = duration_split[-3:]
        if minutes >= 60:
            raise ValueError(f"Minutes in duration exceed 60. Use a value in range: 0-60!")
        if seconds >= 60:
            raise ValueError(f"Seconds in duration exceed 60. Use a value in range: 0-60!")
    elif len(duration_split) >= 2:
        minutes, seconds = duration_split[-2:]
        if seconds >= 60:
            raise ValueError(f"Seconds in duration exceed 60. Use a value in range: 0-60!")
    else:
        seconds = duration_split[-1]

    return hours * 3600 + minutes * 60 + seconds


def parse_distance(distance_str: str) -> float:
    """ Parse a distance string into total meter.

    Args:
        distance_str (str): Distance string with containing unit.
                            Possible units: km, k, m

    Returns:
        float: Distance in meters.

    Raises:
        ValueError: If the input format is invalid or cannot be converted to float.
    """
    distance_str = distance_str.strip().lower()
    
    # Initialize variables
    distance_num_str = ""
    distance_in_km = False
    
    # Check for valid units and extract numeric part
    if distance_str.endswith("km"):
        distance_num_str = distance_str[:-2].strip()
        distance_in_km = True
    elif distance_str.endswith("k"):
        distance_num_str = distance_str[:-1].strip()
        distance_in_km = True
    elif distance_str.endswith("m"):
        distance_num_str = distance_str[:-1].strip()
        distance_in_km = False
    else:
        raise ValueError(f"Given distance '{distance_str}' can't be parsed to a distance! Please use format: '<number><unit>' where unit is 'km', 'k' or 'm'.")
    
    # Validate that we have a numeric part
    if not distance_num_str:
        raise ValueError(f"Given distance '{distance_str}' contains no numeric value! Please use format: '<number><unit>' where unit is 'km', 'k' or 'm'.")
    
    # Use regex pattern that supports decimal numbers (not just integers)
    float_pattern = r'^[+-]?(?:\d+\.?\d*|\.\d+)$'
    if not re.match(float_pattern, distance_num_str):
        raise ValueError(f"Given distance '{distance_str}' contains invalid numeric value '{distance_num_str}'! Please use a valid number with unit 'km', 'k' or 'm'.")
    
    # Safe conversion to float with additional validation
    distance_value = float(distance_num_str)
    
    # Check for negative values
    if distance_value < 0:
        raise ValueError(f"Distance cannot be negative: {distance_value}")
    
    # Convert to meters
    if distance_in_km:
        return distance_value * 1000.0
    return distance_value
