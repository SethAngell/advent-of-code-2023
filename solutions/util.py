def read_from_file(file_path: str) -> list:
    with open(file_path, "r") as ifile:
        return ifile.readlines()


def write_to_file(file_path: str, content: list):
    content = [f"{line}\n" for line in content]
    with open(file_path, "w") as ofile:
        ofile.writelines(content)
