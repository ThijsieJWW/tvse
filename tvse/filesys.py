import os
import pathlib
import sys

__all__ = [
    "File",
    "Directory",
    "FileSystem",
]


class Path:
    ...


class VirtualFileIO:
    ...


class File:
    ...


class Directory:
    ...


class FileSystem:
    ...


class Path(pathlib.Path):
    def is_posix(self) -> bool:
        if os.name == "posix":
            return True
        return False

    def is_nt(self) -> bool:
        if os.name == "nt":
            return True
        return False


class VirtualFileIO:
    __file: File
    __content: bytes
    __encoding: str
    __mode: int
    __bin: bool

    def __init__(
        self, file: File, mode: str, content: bytes, encoding: str = "utf-16"
    ) -> None:
        self.__file = file
        self.__content = content
        self.__encoding = encoding

        if "b" in mode:
            self.__bin = True
        else:
            self.__bin = False
        if "+" in mode:
            self.__mode = 2
        elif "r" in mode:
            self.__mode = 0
        elif "w" in mode:
            self.__mode = 1

        if self.writable():
            self.__content = bytes("", encoding)

    def binary(self) -> bool:
        return self.__bin == True

    def readable(self) -> bool:
        if self.__mode == 1:
            return False
        return True

    def read(self, size: int | None = None) -> str | bytes:
        if self.readable():
            return

        read_c: bytes | str = None
        if self.binary():
            read_c = self.__content
        else:
            read_c = self.__content.decode(self.__encoding)

        if size == None:
            return read_c
        else:
            return read_c[:size]

    def readlines(self, size: int | None = None) -> str | bytes:
        return self.read(size).splitlines()

    def writable(self) -> bool:
        if self.__mode == 0:
            return False
        return True

    def write(self, s: str | bytes) -> int:
        if not self.writable:
            return -1

        if type(s) != type(self.__content):
            return -1

        if not self.binary():
            s = s.encode(self.__encoding)

        self.__content += s
        return 0

    def writelines(self, s: list[str | bytes]) -> int:
        return self.write("\n".join(s))


class File:
    __name: str
    __is_open: bool
    __content: bytes
    __parent: Directory

    def __init__(self, name: str) -> None:
        self.set_name(name)
        self.__is_open = False

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        if type(name) != str:
            raise TypeError("File name must be str.")

        self.__name = name

    def open(self, mode: str) -> VirtualFileIO:
        return VirtualFileIO(self, mode, self.__content)

    def close() -> None:
        pass


class Directory:
    __files: list[File]
    __directories: list[Directory]

    def __init__(self) -> None:
        pass


class FileSystem:
    label: str
    pod: pathlib.Path
    directories: list[Directory]

    def __init__(self, label: str, pod: str) -> None:
        self.label = label
        self.pod = pathlib.Path(pod)
        self.directories = []

    def load(self) -> int:
        """
        (Re)loads the filesystem from a file.
        Returns integer codes representing the status instead of raising exception. codes:
        - 0: Successfull.
        - -1: The file does not exist.
        - -2: The path does not represent a file.
        """
        if not self.pod.exists():
            return -1
        if not self.pod.is_file():
            return -2

        return 0
