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
