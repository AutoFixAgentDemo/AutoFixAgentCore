from ..base.core.add_requirement import UserRequirement
from ..base.core.role import Role
from ..base.core.schema import Message


class Reader(Role):
    """
    A reader to read the vulnerable code and tell the repairer what to do by generating a report.
    """
    name: str = "Reader"
    profile: str = "A reader to read the vulnerable code and tell the repairer what to do by generating a report."
    goal: str = "Read the function contains the sink point in the vulnerable code and generate a report."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([])  # TODO: Fill the actions after implementation
        self._watch([UserRequirement, ])  # TODO: Add the final action in the test to create a loop
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        pass
