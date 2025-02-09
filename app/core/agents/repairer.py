from base.core.add_requirement import UserRequirement
from base.core.role import Role
from base.core.schema import Message
from base.core.action import Action
from core.model.repair import OverallRepair
from .actions.read_code import ReadCode
from .actions.repair import GeneralRepair
from core.model.vuln_report import VulnReport, SingleVuln
from core.model.read_report import ReadReport
from base.core.logs import logger

class Repairer(Role):
    """
    A professional who can repair the vulnerable code and explain.
    """
    name: str = "Repairer"
    profile: str = "A professional who can repair the vulnerable code and explain."
    goal: str = "Understand the vulnerbility and repair it without modification of the original function."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([GeneralRepair])  # TODO: Fill the actions after implementation
        self._watch([ReadCode, ])  # TODO: Add the final action in the test to create a loop
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(
            f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})"
        )  # Print the next action for debugging
        todo = self.rc.todo
        # Add the action to the agent
        if todo.name=="GeneralRepair":
            try:
                code_text=self.rc.memory.get_by_label("vuln_code")[-1].content
                # FIXME: should the vuln_reports should be saved saperately or all-in-one?
                vuln_reports=VulnReport(**{"vulnerabilities":[SingleVuln.model_validate_json(rep.content) for rep in self.rc.memory.get_by_label("vuln_report")]}) # Get all the reports input
                # Extract read report
                read_report_raw=self.rc.memory.get_by_label("read_report")[-1]
                #logger.debug(f"Current memory:{type(read_report_raw)}:{read_report_raw.content}")
                read_reports=ReadReport.model_validate_json(read_report_raw.content)
                res=await todo.run(code_text,vuln_reports,read_reports)
            except Exception as e:
                logger.error(f"Error in reading the vuln_code, vuln_report and read_reports: {e}")
                return None
            res_plain=res.model_dump_json()
            repair_report_msg=Message(content=res_plain,label="repair_report",role=self.name,cause_by=type(todo),sent_from=type(todo))
            self.rc.memory.add(repair_report_msg)
            logger.info(f"Repair report generated and has been pushed to the memory.")
        else:
            # NOTE: Process any unexpected status
            logger.exception(f"Action {self.rc.todo.name} is not implemented or excepted.")
            repair_report_msg = None
        return repair_report_msg