MIN_SCORE: float = 0
MAX_SCORE: float = 100

MIN_STUDENTS: int = 1
MAX_STUDENTS: int = 100

def get_valid_integer(prompt: str, minimum: int, maximum: int) -> int:
    """Prompt the user until a valid integer within [minimum, maximum] is entered.

    Handles non-integer input gracefully and displays a clear error message before re-prompting.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print(
                f"Invalid input. Please enter a whole number "
                f"between {minimum} and {maximum}."
            )
            continue

        if value < minimum or value > maximum:
            print(
                f"Invalid input. Please enter a value "
                f"between {minimum} and {maximum}."
            )
            continue

        return value

def get_valid_float(prompt: str, minimum: float, maximum: float) -> float:
    """Prompt the user until a valid numeric value within [minimum, maximum] is entered.

    Accepts both integer and decimal input. Handles non-numeric input
    gracefully and displays a clear error message before re-prompting.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print(
                f"Invalid input. Please enter a numeric value "
                f"between {int(minimum)} and {int(maximum)}."
            )
            continue

        if value < minimum or value > maximum:
            print(
                f"Invalid input. Please enter a value "
                f"between {int(minimum)} and {int(maximum)}."
            )
            continue

        return value

def get_valid_name(prompt: str) -> str:
    """Prompt the user until a non-empty name is entered.

    Leading and trailing whitespace is stripped before validation.
    """
    while True:
        name = input(prompt).strip()
        if not name:
            print("Student name cannot be empty. Please enter a valid name.")
            continue
        return name
