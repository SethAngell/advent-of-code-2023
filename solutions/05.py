from util import read_from_file, write_to_file, get_input_file


class Range(object):
    def __init__(self, raw_range: str):
        range_pieces = [int(value) for value in raw_range.split(" ") if value != ""]
        self.valid_input_start = range_pieces[1]
        self.valid_input_end = self.valid_input_start + range_pieces[2]
        self.destination_start = range_pieces[0]


class TransitionMap(object):
    def __init__(self, state_title: str, transitional_ranges: list[str]):
        self.raw_ranges = transitional_ranges
        front_half = state_title.split(" ")[0].split("-")
        self.starting_state = front_half[0]
        self.ending_state = front_half[-1]

    def __str__(self):
        return f"{self.starting_state.upper():<12} -> {self.ending_state.upper():<12}"


class Pipeline(object):
    def __init__(self, name: str, seeds: list[int]):
        self.name = name
        self.seeds = seeds
        self.pipeline = []

    def add_transition(self, new_state: TransitionMap):
        self.pipeline.append(new_state)

    def __str__(self):
        return f"Pipeline: {self.name}"


if __name__ == "__main__":
    almanac_page = read_from_file(get_input_file("05"))
    seed_list = almanac_page[0]
    almanac_page = almanac_page[1:]

    pipeline = Pipeline("Seed Pipeline", seed_list)

    state_name = ""
    state_phases = []
    for line in almanac_page:
        if line == "":
            continue

        if line[0].isdigit():
            state_phases.append(line)
        elif line[0].isalpha() and state_name == "":
            print("hi")
            state_name = line
        elif line[0].isalpha() and state_name != "":
            print("hi but with rizz")
            new_state = TransitionMap(state_name, state_phases)
            pipeline.add_transition(new_state)

            state_name = line
            state_phases = []

    print(pipeline)
    for state in pipeline.pipeline:
        print(state)
