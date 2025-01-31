#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/12 00:30
@Author  : alexanderwu
@File    : team.py
@Modified By: mashenquan, 2023/11/27. Add an archiving operation after completing the project, as specified in
        Section 2.2.3.3 of RFC 135.
"""

import warnings
from pathlib import Path
from typing import Any, Optional, List, Tuple

from .add_requirement import UserRequirement
from .const import MESSAGE_ROUTE_TO_ALL, SERDESER_PATH
from .context import Context
from .environment import Environment
from .logs import logger
from .role import Role
from .schema import Message
from .utils.common import (
    NoMoneyException,
    read_json_file,
    serialize_decorator,
    write_json_file,
)
from pydantic import BaseModel, ConfigDict, Field


class Team(BaseModel):
    """
    Team: Possesses one or more roles (agents), SOP (Standard Operating Procedures), and a env for instant messaging,
    dedicated to env any multi-agent activity, such as collaboratively writing executable code.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    env: Optional[Environment] = None
    investment: float = Field(default=10.0)
    idea: str = Field(default="")

    def __init__(self, context: Context = None, **data: Any):
        super(Team, self).__init__(**data)
        ctx = context or Context()
        if not self.env:
            self.env = Environment(context=ctx)
        else:
            self.env.context = ctx  # The `env` object is allocated by deserialization
        if "roles" in data:
            self.hire(data["roles"])
        if "env_desc" in data:
            self.env.desc = data["env_desc"]

    def serialize(self, stg_path: Path = None):
        stg_path = SERDESER_PATH.joinpath("team") if stg_path is None else stg_path
        team_info_path = stg_path.joinpath("team.json")
        serialized_data = self.model_dump()
        serialized_data["context"] = self.env.context.serialize()

        write_json_file(team_info_path, list(
            serialized_data.values()))  # NOTE: Extract all the values from the dictionary and store them in a list

    @classmethod
    def deserialize(cls, stg_path: Path, context: Context = None) -> "Team":
        """stg_path = ./storage/team"""
        # recover team_info
        team_info_path = stg_path.joinpath("team.json")
        if not team_info_path.exists():
            raise FileNotFoundError(
                "recover storage meta file `team.json` not exist, "
                "not to recover and please start a new project."
            )

        team_info: dict = read_json_file(team_info_path)
        ctx = context or Context()
        ctx.deserialize(team_info.pop("context", None))
        team = Team(**team_info, context=ctx)
        return team

    def hire(self, roles: list[Role]):
        """Hire roles to cooperate"""
        self.env.add_roles(roles)

    @property
    def cost_manager(self):
        """Get cost manager"""
        return self.env.context.cost_manager

    def invest(self, investment: float):
        """Invest company. raise NoMoneyException when exceed max_budget."""
        self.investment = investment
        self.cost_manager.max_budget = investment
        logger.info(f"Investment: ${investment}.")

    def _check_balance(self):
        if self.cost_manager.total_cost >= self.cost_manager.max_budget:
            raise NoMoneyException(
                self.cost_manager.total_cost,
                f"Insufficient funds: {self.cost_manager.max_budget}",
            )

    def run_project(self, idea: str, initial_messages: List[Tuple], send_to: str = ""):
        """
        Executes the project initialization process by storing an idea and publishing initial messages to the environment.

        :param idea: A string representing the main concept or goal of the project.
        :param initial_messages: A list of tuples, where each tuple contains:
            - label (str): A descriptor for the message (e.g., "Task", "Info").
            - content (str): The content or body of the message.
        :param send_to: (Optional) A string specifying the recipient(s) of the messages. Defaults to an empty string,
            which will result in the message being sent to all recipients.
        :return: None
        """
        self.idea = idea

        # Push each initial message to the memory
        for message in initial_messages:
            label, content = message
            self.env.publish_message(
                Message(
                    role="Human",
                    label=label,
                    content=content,
                    cause_by=UserRequirement,
                    send_to=send_to or MESSAGE_ROUTE_TO_ALL,
                ),
                peekable=False,
            )
            logger.debug(f"Push an initial message to the memory:{label=},{content=}")
        """# Human requirement.
        self.env.publish_message(
            Message(
                role="Human",
                label="idea",
                content=idea,
                cause_by=UserRequirement,
                send_to=send_to or MESSAGE_ROUTE_TO_ALL,
            ),
            peekable=False,
        )
        self.env.publish_message(
            Message(
                role="Human",
                label="code_path",
                content=str(file_path),
                cause_by=UserRequirement,
                send_to=send_to or MESSAGE_ROUTE_TO_ALL,
            ),
            peekable=False,
        )

        self.env.publish_message(
            Message(
                role="Human",
                label="code",
                content=content,
                cause_by=UserRequirement,
                send_to=send_to or MESSAGE_ROUTE_TO_ALL,
            ),
            peekable=False,
        )"""

    @serialize_decorator
    async def run(self, n_round=3, idea="", send_to="", auto_archive=True):
        """Run company until target round or no money"""
        if idea:
            self.run_project(idea=idea, send_to=send_to)

        while n_round > 0:
            n_round -= 1
            self._check_balance()
            await self.env.run()

            logger.debug(f"max {n_round=} left.")
        self.env.archive(auto_archive)
        return self.env.history
