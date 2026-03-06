import argparse
from api_game import RPSHandler, parse_choice_from_body, parse_choice_from_path, run_api
from game_logic import (
	CHOICES,
	VALID_BEST_OF,
	WINNING_MATCHUPS,
	determine_winner,
	normalize_choice,
	play_round,
	rounds_to_win,
)
from terminal_game import (
	choice_from_menu,
	configure_output,
	format_outcome_message,
	format_score,
	menu_text,
	play_match,
	print_banner,
	prompt_best_of,
	prompt_user_choice,
	run_terminal_game,
	style,
	supports_color,
)


def parse_args():
	parser = argparse.ArgumentParser(description="Rock Paper Scissors Lizard Spock game")
	parser.add_argument("--mode", choices=["cli", "api"], default="cli", help="Run interactive game or REST API")
	parser.add_argument("--host", default="127.0.0.1", help="API host when --mode api")
	parser.add_argument("--port", default=8000, type=int, help="API port when --mode api")
	parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors in terminal output")
	return parser.parse_args()


def main():
	arguments = parse_args()
	if arguments.mode == "api":
		run_api(arguments.host, arguments.port)
	else:
		run_terminal_game(no_color=arguments.no_color)


if __name__ == "__main__":
	main()
