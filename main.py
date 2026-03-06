# Write a rock, paper, scissors game

# import random module
import argparse
import json
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


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


def menu_text():
	return (
		"Choose your option:\n"
		"1. Rock\n"
		"2. Paper\n"
		"3. Scissors\n"
		"4. Lizard\n"
		"5. Spock"
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


def rounds_to_win(best_of):
	if best_of not in VALID_BEST_OF:
		raise ValueError("Best-of value must be 1, 3, or 5.")
	return (best_of // 2) + 1


def prompt_best_of(input_func=input, print_func=print):
	print_func("Choose match length:")
	print_func("1. Best of 1")
	print_func("2. Best of 3")
	print_func("3. Best of 5")
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

	while user_wins < needed_wins and computer_wins < needed_wins:
		print_func(f"\nRound {round_number} (Best of {best_of})")

		while True:
			try:
				user_choice = prompt_user_choice(input_func=input_func, print_func=print_func)
				break
			except ValueError as exc:
				print_func(f"Invalid input: {exc}")

		result = play_round(user_choice, rng=rng)
		print_func(f"You chose: {result['user_choice']}")
		print_func(f"Computer chose: {result['computer_choice']}")
		print_func(result["message"])

		if result["outcome"] == "win":
			user_wins += 1
			round_number += 1
		elif result["outcome"] == "lose":
			computer_wins += 1
			round_number += 1
		else:
			print_func("Tie round: score stays the same, replaying this round.")

		print_func(f"Score -> You: {user_wins} | Computer: {computer_wins}")

	game_winner = "user" if user_wins > computer_wins else "computer"
	return {
		"best_of": best_of,
		"needed_wins": needed_wins,
		"user_wins": user_wins,
		"computer_wins": computer_wins,
		"winner": game_winner,
	}


def parse_choice_from_path(path):
	path_choice = path.lstrip("/").strip().lower()
	if path_choice in CHOICES:
		return path_choice
	raise ValueError("Path must be one of /rock, /paper, /scissors, /lizard, /spock or /play")


def parse_choice_from_body(body_bytes):
	try:
		payload = json.loads(body_bytes.decode("utf-8") or "{}")
	except (json.JSONDecodeError, UnicodeDecodeError) as exc:
		raise ValueError("Request body must be valid JSON.") from exc

	if not isinstance(payload, dict) or "choice" not in payload:
		raise ValueError("JSON body must contain a 'choice' field.")

	return normalize_choice(payload["choice"])


class RPSHandler(BaseHTTPRequestHandler):
	def _write_json(self, status_code, payload):
		encoded = json.dumps(payload).encode("utf-8")
		self.send_response(status_code)
		self.send_header("Content-Type", "application/json")
		self.send_header("Content-Length", str(len(encoded)))
		self.end_headers()
		self.wfile.write(encoded)

	def do_POST(self):
		try:
			if self.path == "/play":
				content_length = int(self.headers.get("Content-Length", "0"))
				body = self.rfile.read(content_length)
				user_choice = parse_choice_from_body(body)
			else:
				user_choice = parse_choice_from_path(self.path)

			self._write_json(200, play_round(user_choice))
		except ValueError as exc:
			self._write_json(400, {"error": str(exc)})

	def do_GET(self):
		self._write_json(
			200,
			{
				"message": "Use POST /play with JSON {'choice': 'rock'} or POST /rock|/paper|/scissors|/lizard|/spock",
				"choices": list(CHOICES),
			},
		)

	def log_message(self, format_, *args):
		# Keep terminal output clean for workshop usage.
		return


def run_api(host="127.0.0.1", port=8000):
	server = ThreadingHTTPServer((host, port), RPSHandler)
	print(f"API listening on http://{host}:{port}")
	print("POST /play with JSON body, or POST /rock|/paper|/scissors|/lizard|/spock")
	server.serve_forever()


# define main function that handles all the logic
def main():
	print("Welcome to Rock, Paper, Scissors, Lizard, Spock!")
	try:
		best_of = prompt_best_of()
	except ValueError as exc:
		print(f"Invalid input: {exc}")
		return

	match_result = play_match(best_of)
	print("\nFinal Result")
	print(f"Best of: {match_result['best_of']}")
	print(f"Final Score -> You: {match_result['user_wins']} | Computer: {match_result['computer_wins']}")
	if match_result["winner"] == "user":
		print("Game winner: You")
	else:
		print("Game winner: Computer")
	print("Game over.")


def parse_args():
	parser = argparse.ArgumentParser(description="Rock Paper Scissors Lizard Spock game")
	parser.add_argument("--mode", choices=["cli", "api"], default="cli", help="Run interactive game or REST API")
	parser.add_argument("--host", default="127.0.0.1", help="API host when --mode api")
	parser.add_argument("--port", default=8000, type=int, help="API port when --mode api")
	return parser.parse_args()


# call main function
if __name__ == "__main__":
	arguments = parse_args()
	if arguments.mode == "api":
		run_api(arguments.host, arguments.port)
	else:
		main()
