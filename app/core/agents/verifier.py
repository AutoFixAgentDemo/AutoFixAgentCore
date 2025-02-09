from base.core.add_requirement import UserRequirement
from base.core.role import Role
from base.core.schema import Message
from base.core.logs import logger

from core.agents.actions.verify import GeneralVerify
from core.agents.actions.repair import GeneralRepair
from core.model.vuln_report import VulnReport, SingleVuln
from core.model.read_report import ReadReport
from core.model.repair import OverallRepair

class Verifier(Role):
    """
    A verifier to verify the repaired code and tell the user if the code is repaired or not.
    """
    name: str = "Verifier"
    profile: str = "A verifier to verify the repaired code and tell the user if the code is repaired or not."
    goal: str = "Verify the repaired code and tell the user if the code is repaired or not, plus check if the patch modifies the original function."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([GeneralVerify])  # TODO: Fill the actions after implementation
        self._watch([GeneralRepair, ])  # TODO: Add the final action in the test to create a loop
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")  # Print the next action for debugging
        todo = self.rc.todo
        # Add the action to the agent
        if self.rc.todo.name=="GeneralVerify":
            try:
                code_text=self.rc.memory.get_by_label("vuln_code")[-1].content
                # NOTE: reports is a VulnReport object
                vuln_reports=VulnReport(**{"vulnerabilities":[SingleVuln.model_validate_json(rep.content) for rep in self.rc.memory.get_by_label("vuln_report")]}) # Get all the reports input
                # Extract read report
                read_reports=ReadReport.model_validate_json(self.rc.memory.get_by_label("read_report")[-1].content)
                repair_reports=OverallRepair.model_validate_json(self.rc.memory.get_by_label("repair_report")[-1].content)
                res=await todo.run(code_text=code_text,vuln_reports=vuln_reports,read_reports=read_reports,diff_texts=repair_reports)
                res_plain=res.model_dump_json()
                verify_report_msg=Message(content=res_plain,label="verify_report",role=self.name,cause_by=type(todo),sent_from=type(todo))
                self.rc.memory.add(verify_report_msg)
                logger.info(f"Verify report generated and has been pushed to the memory.")
            except Exception as e:
                logger.error(f"Error in reading the vuln_code and vuln_report: {e}")
                return None
        else:
            # NOTE: Process any unexpected status
            logger.exception(f"Action {self.rc.todo.name} is not implemented or excepted.")
            verify_report_msg = None
        return verify_report_msg
