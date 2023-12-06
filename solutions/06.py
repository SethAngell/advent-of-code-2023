from util import read_from_file, get_input_file
from math import prod

SPEED_MULTIPLIER = 1


def seek(times: list[int], target: int, time_allowed: int) -> int:
    success = 0
    for time in times:
        speed = time * SPEED_MULTIPLIER
        distance = (time_allowed - time) * speed
        if distance > target:
            success += 1
        else:
            return success


def seek_false(times: list[int], target: int, time_allowed: int) -> int:
    misses = 0
    for time in times:
        speed = time * SPEED_MULTIPLIER
        distance = (time_allowed - time) * speed
        if distance <= target:
            misses += 1
        else:
            return misses

    return misses


if __name__ == "__main__":
    data = read_from_file(get_input_file("06"))
    times = data[0].split(":")[-1]
    records = data[1].split(":")[-1]

    full_time = int(times.replace(" ", ""))
    full_record = int(records.replace(" ", ""))

    times = [int(time) for time in times.split(" ") if time != ""]
    records = [int(record) for record in records.split(" ") if record != ""]

    ways_to_win = []
    for i in range(0, len(times)):
        time = times[i]
        record = records[i]
        middle_point = time // 2
        potential_wins = 0
        potential_wins += seek(
            [time for time in range(middle_point, -1, -1)], record, time
        )
        potential_wins += seek(
            [time for time in range(middle_point + 1, time)], record, time
        )
        ways_to_win.append(potential_wins)

    unkerned_center = full_time // 2

    ways_to_lose = seek_false(
        [time for time in range(0, unkerned_center)], full_record, full_time
    ) + seek_false(
        [time for time in range(full_time, unkerned_center, -1)],
        full_record,
        full_time,
    )

    print(f"There are {prod(ways_to_win):,} ways to win!")
    print(f"There are {(full_time+1)-ways_to_lose:,} ways to win the mega race")
