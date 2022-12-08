#!/usr/bin/env python3


from typing import List, Dict, Union


class Directory:
    def __init__(self, name: str, parent: Union["Directory", None] = None):
        self.name = name
        self.parent = parent
        self.files: Dict[str, int] = {}
        self.sub_dirs: Dict[str, "Directory"] = {}

    def add_file(self, file_name: str, file_size: int) -> None:
        if file_name not in self.files:
            self.files[file_name] = file_size

    def add_dir(self, sub_dir_name: str) -> None:
        if sub_dir_name not in self.sub_dirs:
            self.sub_dirs[sub_dir_name] = Directory(sub_dir_name, self)

    def get_size(self) -> int:
        size = 0
        for _, sd in self.sub_dirs.items():
            size += sd.get_size()
        size += sum(self.files.values())
        return size


ROOT_DIR = Directory("/")


def cd(dir_name: str, current_dir: Directory) -> Directory:
    if dir_name == "/":
        current_dir = ROOT_DIR
    elif dir_name == "..":
        if current_dir.parent is not None:
            current_dir = current_dir.parent
        else:
            assert False, "Parent is None"
    else:
        assert dir_name in current_dir.sub_dirs, f"Directory {dir_name} not present in directory {current_dir.name}"
        current_dir = current_dir.sub_dirs[dir_name]
    return current_dir


def ls(current_dir: Directory):
    pass


def handle_line(line: str, current_dir: Directory) -> Directory:
    line_parts = line.strip().split()
    if line_parts[0] == "$":
        assert len(line_parts) >= 2
        if line_parts[1] == "cd":
            assert len(line_parts) == 3
            current_dir = cd(line_parts[2], current_dir)
        elif line_parts[1] == "ls":
            assert len(line_parts) == 2
            ls(current_dir)
        else:
            assert False
    else:
        if line_parts[0].isnumeric():
            assert len(line_parts) == 2
            current_dir.add_file(line_parts[1], int(line_parts[0]))
        elif line_parts[0] == "dir":
            assert len(line_parts) == 2
            current_dir.add_dir(line_parts[1])
        else:
            assert False
    return current_dir


def get_dir_sizes(dir_sizes: List[int], dir: Directory):
    dir_sizes.append(dir.get_size())
    for _, sub_dir in dir.sub_dirs.items():
        get_dir_sizes(dir_sizes, sub_dir)


def main():
    current_dir = ROOT_DIR
    with open("input.txt", "r") as f:
        for line in f:
            current_dir = handle_line(line, current_dir)
    dir_sizes = []
    get_dir_sizes(dir_sizes, ROOT_DIR)
    selected_dir_sizes = [dir_size for dir_size in dir_sizes if dir_size <= 100000]
    print(sum(selected_dir_sizes))


if __name__ == "__main__":
    main()
