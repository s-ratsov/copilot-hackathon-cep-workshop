import random


CHOICES = ("rock", "paper", "scissors", "lizard", "spock")
VALID_BEST_OF = (1, 3, 5)
WINNING_MATCHUPS = {
    "rock": {"scissors", "lizard"},
    "paper": {"rock", "spock"},
    "scissors": {"paper", "lizard"},
    "lizard": {"paper", "spock"},
    "spock": {"rock", "scissors"},
}


def normalize_choice(value):
    """Normalize and validate a game choice string."""
    if not isinstance(value, str):
        raise ValueError("Choice must be a string.")

    choice = value.strip().lower()
    if choice not in CHOICES:
        raise ValueError(f"Invalid choice: {value}")
    return choice


def determine_winner(user_choice, computer_choice):
    """Return win/lose/tie for a round of RPSLS."""
    user = normalize_choice(user_choice)
    computer = normalize_choice(computer_choice)

    if user == computer:
        return "tie"
    if computer in WINNING_MATCHUPS[user]:
        return "win"
    return "lose"


def play_round(user_choice, computer_choice=None, rng=None):
    """Play one round and return a structured result."""
    user = normalize_choice(user_choice)
    random_generator = rng if rng is not None else random
    computer = normalize_choice(computer_choice) if computer_choice is not None else random_generator.choice(CHOICES)
    outcome = determine_winner(user, computer)

    message = {
        "win": "You win!",
        "lose": "Computer wins!",
        "tie": "It's a tie!",
    }[outcome]

    return {
        "user_choice": user,
        "computer_choice": computer,
        "outcome": outcome,
        "message": message,
    }


def rounds_to_win(best_of):
    if best_of not in VALID_BEST_OF:
        raise ValueError("Best-of value must be 1, 3, or 5.")
    return (best_of // 2) + 1
