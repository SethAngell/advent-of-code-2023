from util import read_from_file, write_to_file


class Game(object):
    def __init__(self, recorded_game: str, output_ledger: list):
        sanitized_record = recorded_game.strip().replace("\n", "")

        self.output_ledger = output_ledger
        self.game_id = self._get_id(sanitized_record.split(":")[0])
        self.output_ledger.append(f"{sanitized_record = }")
        self.drawings = self._get_drawings(sanitized_record.split(":")[-1])
        self.largest_red = 0
        self.largest_green = 0
        self.largest_blue = 0
        self.power_of_game = 0
        self._get_largest_values_from_each_round()
        self._calculate_power()

    def _get_id(self, prefix: str) -> int:
        return int(prefix.split(" ")[-1])

    def _get_drawings(self, suffix: str) -> list[str]:
        self.output_ledger.append(f"{suffix = }")
        return suffix.split(";")

    def _get_largest_values_from_each_round(self):
        for round in self.drawings:
            (
                round_red,
                round_green,
                round_blue,
            ) = self._get_color_allocations_from_handful(round.strip())

            self.largest_red = (
                self.largest_red if self.largest_red > round_red else round_red
            )
            self.largest_green = (
                self.largest_green if self.largest_green > round_green else round_green
            )
            self.largest_blue = (
                self.largest_blue if self.largest_blue > round_blue else round_blue
            )

    def _get_color_allocations_from_handful(self, handful: str) -> tuple:
        red = 0
        green = 0
        blue = 0

        for color_group in handful.split(","):
            count, color = color_group.strip().split(" ")

            if color.lower() == "red":
                red = int(count)
            elif color.lower() == "blue":
                blue = int(count)
            elif color.lower() == "green":
                green = int(count)

        return (red, green, blue)

    def _calculate_power(self):
        self.power_of_game = self.largest_red * self.largest_green * self.largest_blue
        self.output_ledger.append(
            f"{self.largest_red = }, {self.largest_green = }, {self.largest_blue = }, {self.power_of_game=}"
        )


class Scenario(object):
    def __init__(
        self,
        red_cubes: int,
        green_cubes: int,
        blue_cubes: int,
        output_ledger: list,
        testing: bool = False,
    ):
        self.red_cubes = red_cubes
        self.green_cubes = green_cubes
        self.blue_cubes = blue_cubes
        self.output_ledger = output_ledger
        self.testing = testing
        self.ledger_path = "inputs/testing.02.txt" if self.testing else "inputs/02.txt"
        self.serialized_ledger = read_from_file(self.ledger_path)
        self.id_sum_of_valid_games = 0
        self.power_sum_of_all_games = 0
        self.valid_games = []
        self.invalid_games = []
        self._validate_all_recorded_games()

    def _validate_all_recorded_games(self) -> list[Game]:
        self.output_ledger.append(f"Received {len(self.serialized_ledger)} games")
        for recorded_game in self.serialized_ledger:
            current_game = Game(recorded_game, self.output_ledger)
            self.power_sum_of_all_games += current_game.power_of_game
            if self._game_was_possible(current_game):
                self.valid_games.append(current_game)
                self.id_sum_of_valid_games += current_game.game_id
            else:
                self.invalid_games.append(current_game)

    def _game_was_possible(self, game_in_question: Game) -> bool:
        return (
            game_in_question.largest_red <= self.red_cubes
            and game_in_question.largest_green <= self.green_cubes
            and game_in_question.largest_blue <= self.blue_cubes
        )

    def __str__(self):
        return f"There were {len(self.valid_games)} valid games, leading to a sum of {self.id_sum_of_valid_games} and a power of {self.power_sum_of_all_games}"


if __name__ == "__main__":
    output = []
    current_scenario = Scenario(12, 13, 14, output, testing=False)
    write_to_file("output/02.txt", output)
    print(current_scenario)
