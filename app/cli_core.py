"""
The main entry to access the core package using CLI. If you dont want to use the FastAPI server, you can use this script to run the core package.
"""
""""""
import asyncio
from os import abort

import json
import typer

from base.core.logs import define_log_level
from base.core.team import Team
from core.model.vuln_report import VulnReport
from core.utils.path_validator import validate_path
from core.agents.reader import Reader
from core.agents.repairer import Repairer
from core.agents.verifier import Verifier

def main(vuln_text: str, vuln_report: VulnReport) -> dict:
    """
    The main entry of the core AutoFix. In this function we will build a multi-agents team to fix the vulnerable code and return the fixed code diff with other metas.
    NOTE: We will fix all the vuln in one time for now.

    :arg vuln_text: The vulnerable code
    :type vuln_text: str
    :arg vuln_report: The report of the vulnerability
    :type vuln_report: VulnReport
    :return: The fixed code diff with other metas.
    :rtype: dict
    """
    team = Team()
    team.hire(
        [Reader(),Repairer(),Verifier()], # TODO: Add the Repairer and Verifier here after implementing them.
    )
    # NOTE: The main entry to build the team and run
    team.invest(investment=100)
    idea_to_run="Understand, fix and verify the vulnerability mentioned in the vulnerability reports and explain the patchs"
    

    async def run_team(idea_to_run):
        """
        Run the AI team project asynchronously.
        """

        # Resolve the paras and prepare to push the message to the team
        msgs=[("vuln_code",vuln_text)]
        for vuln in vuln_report.vulnerabilities:
            msgs.append(("vuln_report",vuln.model_dump_json()))# Serliaze the vuln_report to json_string
        team.run_project(idea_to_run, msgs) # Push all the messages to the team
        await team.run(n_round=3)  # NOTE: Define the maximum round to run

    asyncio.run(run_team(idea_to_run))  # Run the team

    # The real entry of the fixing

    return {"status": "placeholder"}


def main_wrapper(vuln_report_path: str = typer.Option(help="The path of the report", callback=validate_path, )) -> dict:
    """
    The wrapper of the main entry of the core AutoFix. In this function we extract vulnerable code and report from the vuln report and Instantiate it. Then the two key elements will be sent to the real entry for fixing.

    :arg vuln_report_path: The path of the report
    :type vuln_report_path: str
    :return: The fixed code diff with other metas.
    :rtype: dict
    """

    # Load the json report to a dictionary
    try:
        with open(vuln_report_path, "r") as f:
            vuln_report = json.load(f)
        vuln_text = vuln_report["file"]
        report = vuln_report["report"]
    except Exception as e:
        typer.echo(f"Error loading the report: {str(e)}", err=True)
        abort()

    # Validate the report and load
    try:
        vuln_report_parsed = json.loads(report)
        vuln_report = VulnReport(**vuln_report_parsed)
    except Exception as e:
        typer.echo(f"The report does not match the model: {str(e)}", err=True)
        abort() # TODO: Return the 500 and err msg here

    # Call the main entry
    main(vuln_text, vuln_report)
    return {"status": "placeholder"}



if __name__ == "__main__":
    """
    Entry point for the script. The code below is the core logic of the autofix functionality.
    """
    define_log_level(print_level="INFO")  # NOTE: Set the log level to INFO
    typer.run(main_wrapper)
