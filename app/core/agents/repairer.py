from base.core.add_requirement import UserRequirement
from base.core.role import Role
from base.core.schema import Message


class Repairer(Role):
    """
    A professional who can repair the vulnerable code and explain.
    """
    name: str = "Repairer"
    profile: str = "A professional who can repair the vulnerable code and explain."
    goal: str = "Understand the vulnerbility and repair it without modification of the original function."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([])  # TODO: Fill the actions after implementation
        self._watch([UserRequirement, ])  # TODO: Add the final action in the test to create a loop
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        pass
