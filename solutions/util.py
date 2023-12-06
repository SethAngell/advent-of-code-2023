def read_from_file(file_path: str) -> list:
    lines = []
    with open(file_path, "r") as ifile:
        lines = ifile.readlines()

    lines = [line.replace("\n", "") for line in lines]
    return lines


def write_to_file(file_path: str, content: list):
    content = [f"{line}\n" for line in content]
    with open(file_path, "w") as ofile:
        ofile.writelines(content)


def get_input_file(day: str) -> str:
    print(f'1. {f"inputs/{day}.txt":>25}')
    print(f'2. {f"inputs/debug.{day}.txt":>25}')
    print(f'3. {f"inputs/testing.{day}.txt":>25}')

    choice = input("Which file would you like to use? [1-3]: ")

    if choice == "1":
        return f"inputs/{day}.txt"
    elif choice == "2":
        return f"inputs/debug.{day}.txt"
    else:
        return f"inputs/testing.{day}.txt"
