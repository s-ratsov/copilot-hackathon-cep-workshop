import os
import sys

from game_logic import normalize_choice, play_round, rounds_to_win, VALID_BEST_OF


ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_GREEN = "\033[32m"
ANSI_RED = "\033[31m"
ANSI_YELLOW = "\033[33m"
ANSI_CYAN = "\033[36m"

OUTPUT_STYLED = False


def supports_color(stream):
    """Return True when ANSI color output is safe for the provided stream."""
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    term = os.environ.get("TERM", "")
    return term.lower() != "dumb"


def configure_output(use_color=True, stream=None):
    global OUTPUT_STYLED
    target_stream = stream if stream is not None else sys.stdout
    OUTPUT_STYLED = bool(use_color and supports_color(target_stream))


def style(text, color="", bold=False):
    if not OUTPUT_STYLED:
        return text
    prefix = ""
    if bold:
        prefix += ANSI_BOLD
    if color:
        prefix += color
    return f"{prefix}{text}{ANSI_RESET}"


def print_banner(print_func, title):
    line = "=" * 48
    print_func(style(line, ANSI_CYAN))
    print_func(style(title, ANSI_CYAN, bold=True))
    print_func(style(line, ANSI_CYAN))


def format_outcome_message(result):
    if result["outcome"] == "win":
        return style("Result: You win this round!", ANSI_GREEN, bold=True)
    if result["outcome"] == "lose":
        return style("Result: Computer wins this round!", ANSI_RED, bold=True)
    return style("Result: Tie! Replay this round.", ANSI_YELLOW, bold=True)


def format_score(user_wins, computer_wins):
    label = style("Score", ANSI_CYAN, bold=True)
    user = style(str(user_wins), ANSI_GREEN, bold=True)
    computer = style(str(computer_wins), ANSI_RED, bold=True)
    return f"{label} -> You: {user} | Computer: {computer}"


def menu_text():
    return (
        "Choose your move:\n"
        "  1) Rock\n"
        "  2) Paper\n"
        "  3) Scissors\n"
        "  4) Lizard\n"
        "  5) Spock"
    )


def choice_from_menu(selection):
    options = {
        "1": "rock",
        "2": "paper",
        "3": "scissors",
        "4": "lizard",
        "5": "spock",
    }
    if selection not in options:
        raise ValueError("Invalid menu selection.")
    return options[selection]


def prompt_user_choice(input_func=input, print_func=print):
    print_func(menu_text())
    raw = input_func("Enter number (1-5) or choice name: ").strip().lower()

    if raw in {"1", "2", "3", "4", "5"}:
        return choice_from_menu(raw)
    return normalize_choice(raw)


def prompt_best_of(input_func=input, print_func=print):
    print_func(style("Choose match length:", ANSI_CYAN, bold=True))
    print_func("  1) Best of 1")
    print_func("  2) Best of 3")
    print_func("  3) Best of 5")
    raw = input_func("Enter 1, 3, or 5 (or menu number 1-3): ").strip()

    mapping = {
        "1": 1,
        "2": 3,
        "3": 5,
        "5": 5,
    }

    if raw in mapping:
        best_of = mapping[raw]
    else:
        try:
            best_of = int(raw)
        except ValueError as exc:
            raise ValueError("Invalid match length.") from exc

    if best_of not in VALID_BEST_OF:
        raise ValueError("Best-of value must be 1, 3, or 5.")
    return best_of


def play_match(best_of, input_func=input, print_func=print, rng=None):
    needed_wins = rounds_to_win(best_of)
    user_wins = 0
    computer_wins = 0
    round_number = 1
    print_func()
    print_banner(print_func, f"Match Start: Best of {best_of} (first to {needed_wins})")

    while user_wins < needed_wins and computer_wins < needed_wins:
        print_func()
        print_func(style(f"Round {round_number}", ANSI_CYAN, bold=True))

        while True:
            try:
                user_choice = prompt_user_choice(input_func=input_func, print_func=print_func)
                break
            except ValueError as exc:
                print_func(style(f"Invalid input: {exc}", ANSI_YELLOW, bold=True))

        result = play_round(user_choice, rng=rng)
        print_func(f"You chose     : {style(result['user_choice'], ANSI_GREEN, bold=True)}")
        print_func(f"Computer chose: {style(result['computer_choice'], ANSI_RED, bold=True)}")
        print_func(format_outcome_message(result))

        if result["outcome"] == "win":
            user_wins += 1
            round_number += 1
        elif result["outcome"] == "lose":
            computer_wins += 1
            round_number += 1

        print_func(format_score(user_wins, computer_wins))

    game_winner = "user" if user_wins > computer_wins else "computer"
    return {
        "best_of": best_of,
        "needed_wins": needed_wins,
        "user_wins": user_wins,
        "computer_wins": computer_wins,
        "winner": game_winner,
    }


def run_terminal_game(no_color=False, input_func=input, print_func=print):
    configure_output(use_color=not no_color)
    print_banner(print_func, "Rock, Paper, Scissors, Lizard, Spock")
    try:
        best_of = prompt_best_of(input_func=input_func, print_func=print_func)
    except ValueError as exc:
        print_func(style(f"Invalid input: {exc}", ANSI_YELLOW, bold=True))
        return

    match_result = play_match(best_of, input_func=input_func, print_func=print_func)
    print_func()
    print_banner(print_func, "Final Result")
    print_func(f"Match format: Best of {match_result['best_of']}")
    print_func(format_score(match_result["user_wins"], match_result["computer_wins"]))
    if match_result["winner"] == "user":
        print_func(style("Game winner: You", ANSI_GREEN, bold=True))
    else:
        print_func(style("Game winner: Computer", ANSI_RED, bold=True))
    print_func(style("Game over.", ANSI_CYAN))
