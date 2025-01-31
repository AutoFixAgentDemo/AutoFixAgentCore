from ..base.core.add_requirement import UserRequirement
from ..base.core.role import Role
from ..base.core.schema import Message


class Verifier(Role):
    """
    A verifier to verify the repaired code and tell the user if the code is repaired or not.
    """
    name: str = "Verifier"
    profile: str = "A verifier to verify the repaired code and tell the user if the code is repaired or not."
    goal: str = "Verify the repaired code and tell the user if the code is repaired or not, plus check if the patch modifies the original function."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([])  # TODO: Fill the actions after implementation
        self._watch([UserRequirement, ])  # TODO: Add the final action in the test to create a loop
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        pass
