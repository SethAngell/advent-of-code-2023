from util import read_from_file, write_to_file
import json


class ScratchOff(object):
    def __init__(self, data: str):
        split_data = data.split(":")
        prefix = split_data[0]
        suffix = split_data[1]

        self.id = self._get_game_count(prefix)
        self.winning_numbers = self._get_winning_numbers(suffix.split("|")[0])
        self.card_numbers = self._get_card_numbers(suffix.split("|")[-1])

        self.intersection = self._get_intersection()
        self.number_of_wins = len(self.intersection)
        self.score = self._calculate_score()

    def _get_game_count(self, prefix: str):
        return int(prefix.split(" ")[-1])

    def _convert_strings_to_ints(self, nums: list[str]) -> set[int]:
        return set([int(num) for num in nums if num.isdigit()])

    def _get_winning_numbers(self, nums_to_parse: str) -> set[int]:
        split_nums = nums_to_parse.split(" ")
        return self._convert_strings_to_ints(split_nums)

    def _get_card_numbers(self, nums_to_parse: str) -> set[int]:
        split_nums = nums_to_parse.split(" ")
        return self._convert_strings_to_ints(split_nums)

    def _get_intersection(self):
        return self.winning_numbers.intersection(self.card_numbers)

    def _calculate_score(self):
        if len(self.intersection) == 0:
            return 0
        else:
            return 2 ** (len(self.intersection) - 1)

    def __str__(self):
        set_representation = (
            "{}" if len(self.intersection) == 0 else str(self.intersection)
        )
        return f"| #{self.id:<4} | {set_representation:<40} | {len(self.intersection):<10} | {self.score:<5} |"

    def __repr__(self):
        return self.__str__()


def get_input_file() -> str:
    print(f'1. {"inputs/04.txt":>25}')
    print(f'2. {"inputs/testing.04.txt":>25}')
    choice = input("Which file would you like to use? [1-2]: ")

    if choice == "1":
        return "inputs/04.txt"
    else:
        return "inputs/testing.04.txt"


if __name__ == "__main__":
    file_path = get_input_file()
    cards = []
    output = []

    cards_to_parse = read_from_file(file_path=file_path)
    for card in cards_to_parse:
        cards.append(ScratchOff(card))

    header_string = (
        f'| {"ID":<5} | {"Intersections":40} | {"Win Count":10} | {"Score":<5} |'
    )
    output.append("-" * len(header_string))
    output.append(header_string)
    output.append("-" * len(header_string))

    wins = {}
    for card in cards:
        wins[card.id] = 1

    total_winnings = 0
    for card in cards:
        total_winnings += card.score
        base = wins[card.id]
        for win_num in range(1, card.number_of_wins + 1):
            wins[card.id + win_num] = wins[card.id + win_num] + base

        output.append(str(card))
    output.append("-" * len(header_string))

    score_results = f"You won {total_winnings:,} points!"
    output.append(f"| {'RESULTS':16} | {score_results:{50}} |")
    total_cards = sum([win for _, win in wins.items()])
    cards_results = f"You won {total_cards:,} cards!"

    output.append(f"| {'TOTAL CARDS':16} | {cards_results:{50}} |")
    output.append("-" * len(header_string))

    with open("output/04.json", "w") as fp:
        json.dump(wins, fp)

    write_to_file("output/04.txt", output)
