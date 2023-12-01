import re
from util import read_from_file, write_to_file

TESTING = False
DEBUG = True

DIGITS_REGEX = r"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))"
TEST_INPUT = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]
TEXT_TO_INT_MAPPINGS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def normalize_text_into_digit(text_value: str) -> str:
    if text_value.isdigit():
        return text_value

    return TEXT_TO_INT_MAPPINGS[text_value.strip()]


def format_results_for_output(line, matches, produced_value):
    return f"{line:<64} -> {', '.join(matches):<64} -> {produced_value}"


def find_digits(line: str, output: list) -> int:
    line = line.replace("\n", "")
    match = re.findall(DIGITS_REGEX, line)
    if len(match) < 1:
        output.append(format_results_for_output(line, match, "0"))
        return 0
    elif len(match) == 1:
        normalized_value = normalize_text_into_digit(match[0])
        doubled_single_value = normalized_value + normalized_value
        output.append(format_results_for_output(line, match, doubled_single_value))
        return int(doubled_single_value)
    else:
        bookend_values = normalize_text_into_digit(
            match[0]
        ) + normalize_text_into_digit(match[-1])
        output.append(format_results_for_output(line, match, bookend_values))
        return int(bookend_values)


if __name__ == "__main__":
    output = []
    lines_to_decode = TEST_INPUT if TESTING else read_from_file("inputs/01.txt")
    running_sum = 0
    for line in lines_to_decode:
        running_sum += find_digits(line, output)

    print(f"The coordinates are: {running_sum}.")
    if DEBUG:
        write_to_file("output/01.txt", output)
