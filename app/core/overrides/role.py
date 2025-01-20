from metagpt.roles.role import Role

class RoleWithLabel(Role):
    latest_observed_msg: Optional[Message] = None  # record the latest observed message when interrupted