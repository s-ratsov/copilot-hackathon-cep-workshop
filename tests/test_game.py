import json
import unittest

import main


class StubRng:
    def __init__(self, value):
        self.value = value

    def choice(self, _):
        return self.value


class TestGameLogic(unittest.TestCase):
    def test_normalize_choice_accepts_valid_values(self):
        self.assertEqual(main.normalize_choice("  Rock  "), "rock")
        self.assertEqual(main.normalize_choice("SPOCK"), "spock")

    def test_normalize_choice_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            main.normalize_choice("banana")

        with self.assertRaises(ValueError):
            main.normalize_choice(10)

    def test_all_ties(self):
        for choice in main.CHOICES:
            self.assertEqual(main.determine_winner(choice, choice), "tie")

    def test_all_winning_pairs(self):
        for winner, losers in main.WINNING_MATCHUPS.items():
            for loser in losers:
                self.assertEqual(main.determine_winner(winner, loser), "win")
                self.assertEqual(main.determine_winner(loser, winner), "lose")

    def test_play_round_with_forced_computer_choice(self):
        result = main.play_round("rock", computer_choice="scissors")
        self.assertEqual(result["user_choice"], "rock")
        self.assertEqual(result["computer_choice"], "scissors")
        self.assertEqual(result["outcome"], "win")

    def test_play_round_with_stub_rng(self):
        result = main.play_round("lizard", rng=StubRng("spock"))
        self.assertEqual(result["computer_choice"], "spock")
        self.assertEqual(result["outcome"], "win")

    def test_choice_from_menu(self):
        self.assertEqual(main.choice_from_menu("1"), "rock")
        self.assertEqual(main.choice_from_menu("5"), "spock")
        with self.assertRaises(ValueError):
            main.choice_from_menu("8")

    def test_parse_choice_from_path(self):
        self.assertEqual(main.parse_choice_from_path("/paper"), "paper")
        with self.assertRaises(ValueError):
            main.parse_choice_from_path("/invalid")

    def test_parse_choice_from_body(self):
        body = json.dumps({"choice": "Lizard"}).encode("utf-8")
        self.assertEqual(main.parse_choice_from_body(body), "lizard")

    def test_parse_choice_from_body_rejects_bad_payload(self):
        with self.assertRaises(ValueError):
            main.parse_choice_from_body(b"not-json")

        with self.assertRaises(ValueError):
            main.parse_choice_from_body(json.dumps({"move": "rock"}).encode("utf-8"))

    def test_rounds_to_win(self):
        self.assertEqual(main.rounds_to_win(1), 1)
        self.assertEqual(main.rounds_to_win(3), 2)
        self.assertEqual(main.rounds_to_win(5), 3)

        with self.assertRaises(ValueError):
            main.rounds_to_win(7)

    def test_play_match_best_of_three_user_wins(self):
        inputs = iter(["1", "1", "1"])

        def fake_input(_):
            return next(inputs)

        result = main.play_match(3, input_func=fake_input, print_func=lambda *_: None, rng=StubRng("scissors"))
        self.assertEqual(result["winner"], "user")
        self.assertEqual(result["user_wins"], 2)
        self.assertEqual(result["computer_wins"], 0)


if __name__ == "__main__":
    unittest.main()
