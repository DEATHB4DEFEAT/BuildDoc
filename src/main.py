from io import TextIOWrapper
from sys import argv
from console.error import builddoc_error
from utils.mapper import mapper
import os


class main:
    """
    Starting point, where everything needed to initialize BuildDoc is stuffed into this class.
    """

    cwd = os.getcwd()

    def __init__(self) -> None:
        pass

    def check_for_builddoc(self) -> "str | None":
        """
        Checks to see if `./BuildDoc` exists, returning the path to it if it does. If it doesn't,
        `None` is returned.
        """

        try:
            for entry in os.scandir(self.cwd):
                if entry.is_file() and entry.name.lower() == "builddoc":
                    return f"{self.cwd}/BuildDoc"
                else:
                    continue
            return None
        except:
            raise builddoc_error("Internal error (unknown).")  # Just in case.

    def run(self, path: str, task: str) -> None:
        """
        Maps, parses, and runs `task` in the BuildDoc.
        """

        try:
            builddoc: TextIOWrapper = open(path, "r")
            code: str = builddoc.read()

            # Mapping.
            variables: "dict[str, str]" = mapper.map_variables(code)
            commands: "dict[str, list[str]]" = mapper.map_task(code, task)

        except:
            raise builddoc_error("Something went wrong...")
        finally:
            builddoc.close()  # Always close an open file!


if __name__ == "__main__":
    MAIN: main = main()
    path: "str | None" = MAIN.check_for_builddoc()

    try:
        assert path is not None

        if len(argv) > 1:
            MAIN.run(path, argv[1])
        else:
            MAIN.run(path, None)
    except AssertionError:
        raise builddoc_error("No BuildDoc found.")
