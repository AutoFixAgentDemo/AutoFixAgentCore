# Absolute Import
from base.core.add_requirement import UserRequirement
from base.core.role import Role
from base.core.schema import Message
from base.core.logs import logger
from model.vuln_report import VulnReport, SingleVuln

# Relative Import
from .actions.read_code import ReadCode

class Reader(Role):
    """
    A reader to read the vulnerable code and tell the repairer what to do by generating a report.
    """
    name: str = "Reader"
    profile: str = "A reader to read the vulnerable code and tell the repairer what to do by generating a report."
    goal: str = "Read the function contains the sink point in the vulnerable code and generate a report."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([ReadCode])  # TODO: Fill the actions after implementation
        self._watch([UserRequirement, ])  # TODO: Add the final action in the test to create a loop
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(
            f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})"
        )  # Print the next action for debugging
        todo = self.rc.todo
        # Add the action to the agent
        if self.rc.todo.name=="ReadCode":
            try:
                code_text=self.rc.memory.get_by_label("vuln_code")[-1].content
                # NOTE: reports is a VulnReport object
                reports=VulnReport(**[SingleVuln.model_validate_json(rep.content) for rep in self.rc.memory.get_by_label("vuln_report")]) # Get all the reports input
            except Exception as e:
                logger.error(f"Error in reading the vuln_code and vuln_report: {e}")
                return None # TODO: Add error handling here
            # TODO: Run the action and process the response
            await todo.run(code_text=code_text,reports=reports) 
        else:
            # NOTE: Process any unexpected status
            logger.exception(f"Action {self.rc.todo.name} is not implemented or excepted.")
            msg = None
        return msg
