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
    if opt_str.strip().isdigit():
        opt_number = int(opt_str)
        if opt_number in opt.keys():
            return opt_number
        else:
            raise ValueError(f"Option '{opt_number}' is not a valid option!")
    else:
        raise ValueError(f"Option '{opt_str}' is not a valid number!")


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
    predefined_distance_mrt = ['marathon', 'mrt']
    predefined_distance_hmt = ['half marathon', 'half-marathon', 'semi marathon', 'semi-marathon', 'hmt', 'hm']

    distance_str = distance_str.strip().lower()
    
    if distance_str in predefined_distance_mrt:
        return 42195.0
    if distance_str in predefined_distance_hmt:
        return 21097.5

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


def parse_pace(pace_str: str) -> float:
    """
        Parse a pace string into seconds per meter.
        Valid formats are: 
            seconds/km', seconds/m,
            'HH:MM:SS/km', 'HH:MM:SS/m',
            'MM min/km', 'MMmin/m',
            'MM:SS min/km', 'MM:SS min/m',
            'SS sec/km', 'SS sec/m'
    
    Args:
        pace_str (str): Pace string in different formats.

    Returns:
        float: Pace in seconds per meter.

    Raises:
        ValueError: If the input format is invalid.
    """
    pace_str = pace_str.strip().lower()
    if pace_str.endswith("/km"):
        pace_time_str = pace_str[:-3].strip()
        d_factor = 1000.0
    elif pace_str.endswith("/m"):
        pace_time_str = pace_str[:-2].strip()
        d_factor = 1.0
    else:
        raise ValueError(f"Given pace '{pace_str}' can't be parsed to a pace! Please use format: 'MM:SS/km' or 'MM:SS/m'.")

    if pace_time_str.endswith("min"):
        pace_number_str = pace_time_str[:-3].strip()
        pace_number_split = pace_number_str.split(':')
        if len(pace_number_split) >= 2:
            t_factor = 1.0
        else:
            t_factor = 60.0
    elif pace_time_str.endswith("sec"):
        pace_number_str = pace_time_str[:-3].strip()
        t_factor = 1.0
    else:
        pace_number_str = pace_time_str
        t_factor = 1.0

    try:
        total_seconds = t_factor * parse_duration(pace_number_str)
        return total_seconds / d_factor
    except ValueError as e:
        raise ValueError(e)

