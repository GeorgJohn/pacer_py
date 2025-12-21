import pacer_py.user_input_parser as parser

def clear_console() -> None:
    """Clear the console output."""
    print("\n" * 100)


def display_available_options(opt: dict[int, str]) -> None:
        """Display available jobs to the user."""
        print("Available options:")
        print(42 * "-")
        for key, value in opt.items():
            print(f"{key}: {value}")
        print(42 * "-")


def ask_user_for_option(opt: dict[int, str]) -> int:
    """Ask the user to choose from different jobs."""
    for _ in range(3):  # Allow up to 3 attempts
        clear_console()
        display_available_options(opt)
        user_input_str = input("Please choose one of the listed options: ").strip()
        try:
            return parser.parse_option(user_input_str, opt)
        except ValueError as e:
            print(f"{e} Please try again.")

        input("Please try again. Press Enter to continue...")
    return -1  # Indicate failure after 3 attempts


def ask_user_for_distance() -> float:
    """Ask the user for a distance input."""
    for _ in range(3):  # Allow up to 3 attempts
        distance_str = input("Enter distance (e.g., '5km', '3.1m'): ").strip()
        try:
            return parser.parse_distance(distance_str)
        except ValueError as e:
            print(f"{e}, Please try again.")
    raise ValueError("Failed to parse distance after multiple attempts.")
    

def ask_user_for_duration() -> int:
    """Ask the user for a duration input."""
    for _ in range(3):  # Allow up to 3 attempts
        duration_str = input("Enter duration (e.g., '01:02:03', '45'): ").strip()
        try:
            return parser.parse_duration(duration_str)
        except ValueError as e:
            print(f"{e}, Please try again.")
    raise ValueError("Failed to parse duration after multiple attempts.")


def ask_user_for_pace() -> float:
    """Ask the user for a pace input."""
    for _ in range(3):  # Allow up to 3 attempts
        pace_str = input("Enter pace (e.g., '5:00/km', '8:00/m'): ").strip()
        try:
            return parser.parse_pace(pace_str)
        except ValueError as e:
            print(f"{e}, Please try again.")
    raise ValueError("Failed to parse pace after multiple attempts.")
