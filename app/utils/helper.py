from random import random
import string


def random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string of given length."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))