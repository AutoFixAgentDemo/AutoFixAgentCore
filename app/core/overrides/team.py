from metagpt.actions.add_requirement import UserRequirement
from metagpt.const import MESSAGE_ROUTE_TO_ALL
from metagpt.team import Team

from .schema import MessageWithLabel


class TeamWithLabel(Team):
    def run_project(self, idea, send_to: str = ""):
        """Run a project from publishing user requirement."""
        self.idea = idea
        # Human requirement.
        self.env.publish_message(
            MessageWithLabel(role="Human", label="HumanIdea", content=idea, cause_by=UserRequirement,
                             send_to=send_to or MESSAGE_ROUTE_TO_ALL),
            peekable=False,
        )
