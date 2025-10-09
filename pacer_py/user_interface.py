from typing import Any

from pacer_py.user_input_parser import parse_option

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
            return parse_option(user_input_str, opt)
        except ValueError as e:
            print(f"{e} Please try again.")

        input("Please try again. Press Enter to continue...")
    return -1  # Indicate failure after 3 attempts

def ask_user_for_distance() -> str:
    """Ask the user for a distance input."""
    return input("Enter distance (e.g., '5km', '3.1m'): ").strip()

def ask_user_for_duration() -> str:
    """Ask the user for a duration input."""
    return input("Enter duration (e.g., '01:02:03', '45'): ").strip()
