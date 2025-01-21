import pathlib

import typer


def validate_path(path: str) -> pathlib.Path:
    """
    Validates if a given path is a legal and existing path.

    :param path: The path to validate.
    :type path: str

    :return: The path as a pathlib.Path object.
    :rtype: pathlib.Path
    """
    try:
        # Convert to pathlib.Path
        path_obj = pathlib.Path(path)

        # Check if the path exists
        if not path_obj.exists():
            raise typer.BadParameter(f"The path '{path}' does not exist.")
        # Check if the path is a json file
        if path_obj.suffix != ".json":
            raise typer.BadParameter(f"The path '{path}' is not a json file.")
        return path_obj
    except Exception as e:
        raise typer.BadParameter(f"Invalid path: {path}. Error: {str(e)}") from e
