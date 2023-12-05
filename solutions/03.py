from dataclasses import dataclass
import uuid

from util import read_from_file, write_to_file

DEBUG = True
TESTING = True


@dataclass
class PointOfInterest:
    """Class for keeping track POIs in the schematic."""

    id: str
    value: str
    x: int
    y: int


@dataclass
class PartNumber:
    """Class for keeping track of valid part numbers"""

    value: str
    left_edge: int
    right_edge: int
    y: int
    poi: PointOfInterest
    origin: str

    def __hash__(self):
        return int(f"{self.value}{self.left_edge}{self.right_edge}{self.y}")


@dataclass
class Gear:
    """Class for keeping track of gears"""

    part_one: PartNumber
    part_two: PartNumber
    total_value: int

    def get_value(self):
        self.total_value = int(self.part_one.value) * int(self.part_two.value)
        return self.total_value


def find_left(line: list, starting_x: int):
    print(line)
    print(starting_x)
    print(line[starting_x])
    for x in range(starting_x, -1, -1):
        if line[x].isdigit() is False:
            return x + 1

    return 0


def find_right(line: list, starting_x: int):
    end = len(line)
    for x in range(starting_x, end):
        if line[x].isdigit() is False:
            return x

    return len(line)


def select_input_file() -> str:
    print(f'1:{"inputs/03.txt":>30}')
    print(f'2:{"inputs/debug.03.txt":>30}')
    print(f'3:{"inputs/testing.03.txt":>30}')
    choice = input("Which file would you like to test against? [1-3]: ")
    print("\n")

    if choice == "1":
        return "inputs/03.txt"
    elif choice == "2":
        return "inputs/debug.03.txt"
    else:
        return "inputs/testing.03.txt"


def check_top_left(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.y == 0 or poi.x == 0:
        return None

    if schematic[poi.y - 1][poi.x - 1].isdigit() is False:
        return None

    left_edge = find_left(schematic[poi.y - 1], poi.x - 1)
    right_edge = find_right(schematic[poi.y - 1], poi.x - 1)
    value = schematic[poi.y - 1][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y - 1, poi, "TopLeft")


def check_bottom_left(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.y == len(schematic) - 1 or poi.x == 0:
        return None

    if schematic[poi.y + 1][poi.x - 1].isdigit() is False:
        return None

    left_edge = find_left(schematic[poi.y + 1], poi.x - 1)
    right_edge = find_right(schematic[poi.y + 1], poi.x - 1)
    value = schematic[poi.y + 1][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y + 1, poi, "BottomLeft")


def check_left(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.x == 0:
        return None

    if schematic[poi.y][poi.x - 1].isdigit() is False:
        return None

    left_edge = find_left(schematic[poi.y], poi.x - 1)
    right_edge = poi.x
    value = schematic[poi.y][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y, poi, "Left")


def check_top_right(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.y == 0 or poi.x == len(schematic[0]) - 1:
        return None

    if schematic[poi.y - 1][poi.x + 1].isdigit() is False:
        return None

    left_edge = find_left(schematic[poi.y - 1], poi.x + 1)
    right_edge = find_right(schematic[poi.y - 1], poi.x + 1)
    value = schematic[poi.y - 1][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y - 1, poi, "TopRight")


def check_bottom_right(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.y == len(schematic) - 1 or poi.x == len(schematic[0]) - 1:
        return None

    if schematic[poi.y + 1][poi.x + 1].isdigit() is False:
        return None

    left_edge = find_left(schematic[poi.y + 1], poi.x + 1)
    right_edge = find_right(schematic[poi.y + 1], poi.x + 1)
    value = schematic[poi.y + 1][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y + 1, poi, "BottomRight")


def check_right(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.x == len(schematic[0]) - 1:
        return None

    if schematic[poi.y][poi.x + 1].isdigit() is False:
        return None

    left_edge = poi.x + 1
    right_edge = find_right(schematic[poi.y], poi.x + 1)
    value = schematic[poi.y][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y, poi, "Right")


def check_top_middle(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.y == 0:
        return None

    if schematic[poi.y - 1][poi.x].isdigit() is False:
        return None

    left_edge = find_left(schematic[poi.y - 1], poi.x)
    right_edge = find_right(schematic[poi.y - 1], poi.x)
    value = schematic[poi.y - 1][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y - 1, poi, "TopMiddle")


def check_bottom_middle(poi: PointOfInterest, schematic: list) -> PartNumber:
    if poi.y == len(schematic) - 1:
        return None

    if schematic[poi.y + 1][poi.x].isdigit() is False:
        return None

    left_edge = find_left(schematic[poi.y + 1], poi.x)
    right_edge = find_right(schematic[poi.y + 1], poi.x)
    value = schematic[poi.y + 1][left_edge:right_edge]

    return PartNumber(value, left_edge, right_edge, poi.y + 1, poi, "BottomMiddle")


def find_values_around_points_of_interest(
    poi: PointOfInterest, schematic: list
) -> list[PartNumber]:
    potential_part_numbers = []
    potential_part_numbers.append(check_top_middle(poi, schematic))
    potential_part_numbers.append(check_top_left(poi, schematic))
    potential_part_numbers.append(check_left(poi, schematic))
    potential_part_numbers.append(check_bottom_left(poi, schematic))
    potential_part_numbers.append(check_bottom_middle(poi, schematic))
    potential_part_numbers.append(check_top_right(poi, schematic))
    potential_part_numbers.append(check_right(poi, schematic))
    potential_part_numbers.append(check_bottom_right(poi, schematic))

    part_numbers = [
        part_number for part_number in potential_part_numbers if part_number is not None
    ]

    return part_numbers


def filter_for_unique_part_numbers(part_numbers: list[PartNumber]) -> list[PartNumber]:
    unique_part_numbers = {}
    print("IN: " + str(len(part_numbers)))

    for part in part_numbers:
        key = hash(f"{part.value}-{part.poi.id}-{part.left_edge}-{part.right_edge}")
        unique_part_numbers[key] = part

    print("OUT: " + str(len(unique_part_numbers.keys())))
    unique_parts = [value for key, value in unique_part_numbers.items()]
    return unique_parts


def calculate_gear_product(gears: list[Gear]) -> int:
    return sum([gear.get_value() for gear in gears])


def find_gears(part_numbers: list[PartNumber]) -> list[Gear]:
    potential_gears_segment = [part for part in part_numbers if part.poi.value == "*"]
    gear_mappings = {}
    gears = []

    for gear in potential_gears_segment:
        if gear.poi.id in gear_mappings.keys():
            gear_mappings[gear.poi.id].append(gear)
        else:
            gear_mappings[gear.poi.id] = [gear]

    for potential_gear in gear_mappings.keys():
        if len(gear_mappings[potential_gear]) == 2:
            gears.append(
                Gear(
                    gear_mappings[potential_gear][0],
                    gear_mappings[potential_gear][1],
                    0,
                )
            )

    return gears


if __name__ == "__main__":
    file_path = select_input_file()

    points_of_interest = []
    schematic = read_from_file(file_path=file_path)

    for y in range(0, len(schematic)):
        for x in range(0, len(schematic[0])):
            coordinate = schematic[y][x]
            not_a_digit = coordinate.isdigit() is False
            not_a_period = coordinate != "."
            if not_a_digit and not_a_period:
                points_of_interest.append(
                    PointOfInterest(value=coordinate, x=x, y=y, id=uuid.uuid4())
                )

    parts = []
    for poi in points_of_interest:
        print(f"POI: {poi.value} @ ({poi.x},{poi.y})")
        parts += find_values_around_points_of_interest(poi, schematic)

    output = ["=== ALL PARTS ===\n"]
    output.append(f"{len(parts)} parts.")
    output += parts
    output.append("\n=== UNIQUE PARTS ===\n")
    output.append(f"{len(set(parts))} parts.")
    output += set(parts)
    output.append("\n=== GUID ===")
    output.append(f"{len(filter_for_unique_part_numbers(parts))} parts.")
    output += filter_for_unique_part_numbers(parts)
    write_to_file("output/03.txt", output)

    unique_part_numbers = [
        int(part.value) for part in filter_for_unique_part_numbers(parts)
    ]
    print(unique_part_numbers)
    gears = find_gears(filter_for_unique_part_numbers(parts))

    print(f"The sum of all unique parts is: {sum(unique_part_numbers)}")
    print(f"The product of all gears is: {calculate_gear_product(gears)}")
