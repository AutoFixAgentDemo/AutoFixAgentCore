""""""
import typer

from base.core.logs import define_log_level


def main_wrapper(vuln_report_path: str = typer.Option(help="The path of the report")) -> dict:
    """
    The wrapper of the main entry of the core AutoFix. In this function we extract vulnerable code and report from the vuln report and Instantiate it. Then the two key elements will be sent to the real entry for fixing.
    """
    pass


if __name__ == "__main__":
    """
    Entry point for the script. The code below is the core logic of the autofix functionality.
    """
    define_log_level(print_level="INFO")  # NOTE: Set the log level to INFO
    typer.run(main_wrapper)
