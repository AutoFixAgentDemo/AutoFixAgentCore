"""
This script provides a simple example demonstrating how to use the modified MetaGPT library with enhanced label functionality.
The code has been tested with the Qwen-2.5:32B model from the Ollama LLM. Once properly configured, the script should run smoothly without issues.
Refer to the examples provided within this file to develop your own custom implementations using the MetaGPT library.

Description:
This example demonstrates the design and implementation of a single role, `CodeWriter`, with two actions: `SimpleWrite` and `SimpleCheck`.
The purpose of this script is to create a Python code snippet based on a given idea, following a structured process:

Steps:
1. Initialize the team.
2. Push the initial idea into the memory pool.
3. The `CodeWriter` role observes the idea and uses the `SimpleWrite` action to generate a Python code snippet.
4. The `CodeWriter` role then employs the `SimpleCheck` action to validate the generated snippet.
   It provides a conclusion on whether the snippet is correct, along with any issues it identifies.
5. (May not implemented yet): If the answer is "No," the `SimpleWrite` action will be recalled to refine the snippet and restart the process.

Usage:
- Ensure the  Qwen-2.5:32B model are properly installed and configured before running the script.
- Follow the documented examples to extend or adapt the code to your specific requirements.

Note:
- Verify your environment setup before execution to avoid runtime issues.
- Additional documentation for MetaGPT and Qwen-2.5:32B can be found in their respective repositories or official guides.
- Read the comments with `NOTE` carefully for better understanding.
"""
import asyncio
import json
from typing import ClassVar

import fire

from base.core.action import Action
from base.core.add_requirement import UserRequirement
from base.core.logs import define_log_level
from base.core.logs import logger
from base.core.role import Role
from base.core.schema import Message
from base.core.team import Team


class SimpleWrite(Action):
    # NOTE: Implement the action here
    # NOTE: Must specify PROMPT_TEMPLATE as the type of ClassVar[str] to pass the pydantic validation.
    PROMPT_TEMPLATE: ClassVar[str] = """
        Write a Python program to fulfill the following requirement:

        {requirement}

        Please ensure the code is:
        - Well-documented with comments.
        - Modular and uses functions/classes where appropriate.
        - Efficient and follows best practices in Python.

        If there are any edge cases or potential errors, provide handling for those as well.

        Return only the code, with no additional explanation or code fences.
        """

    name: str = "SimpleWrite"  # Be better to
    desc: str = (
        "A detector skilled at identifying vulnerabilities in the provided code snippets."
    )

    async def run(self, idea: str) -> str:
        # NOTE: Rewrite the run method to implement the way to fill the template and start the complementation.
        prompt = self.PROMPT_TEMPLATE.format(requirement=idea)

        rsp = await self._aask(prompt)
        logger.info(f"Response from SimpleWrite: {rsp}")
        return rsp


class SimpleCheck(Action):
    PROMPT_TEMPLATE: ClassVar[str] = """
        The following Python code was generated to fulfill this requirement:

        Requirement:
        {requirement}

        Code:
        {code}

        Please validate whether this code meets the following criteria:
        - Accurately fulfills the requirement.
        - Handles edge cases and potential errors properly.
        - Adheres to best practices and conventions in Python.
        - Is efficient and well-structured.
        - Includes appropriate comments and documentation.

        Respond in JSON format with the following structure without any other parts:
        {{
            "conclusion": "Yes" or "No",  // Whether the code meets the requirement
            "issues": [
                "Description of issue 1",
                "Description of issue 2",
                "..." // List all identified issues, or an empty list if there are none
            ]
        }}
    """
    # NOTE: Use `{{` instead of `{` in strings where the content is not a variable,
    # to prevent KeyError when formatting the string.

    name: str = "SimpleCheck"  # NOTE: Better matching the classname
    desc: str = (
        "A professional Python code reviewer."
    )

    async def run(self, code: str, idea: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(code=code, requirement=idea)
        rsp = await self._aask(prompt)
        logger.info(f"Response from SimpleCheck: {rsp}")
        return rsp


class CodeWriter(Role):
    name: str = "Jason"
    profile: str = "a skilled assistant with expertise in analysis request and write code"
    goal: str = (
        "To analysis the requirement from the user and write code to fulfill the requirement"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # NOTE: Never forget
        self.set_actions([SimpleWrite, SimpleCheck])  # NOTE: register actions belongs to this role
        self._watch([UserRequirement])  # NOTE: Define the actions that trigger the execution of this role.
        self._set_react_mode(react_mode="by_order")  # NOTE: Set the reaction mode from "by_order", "react", etc.

    async def _act(self) -> Message:
        # NOTE: Override the `_act` method to extract memories with specific labels from the memory pool
        # and execute the corresponding actions in separate `if-elif` blocks.
        # This ensures that the `_run` method for each action can handle different parameters as needed.

        logger.info(
            f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})"
        )  # Print the next action for debugging
        todo = self.rc.todo

        # NOTE: Start the action in different case. It is recommended to use if-elif block to process this.
        if self.rc.todo.name == "SimpleWrite":
            try:
                requirement = self.rc.memory.get_by_label("idea")[-1].content
                # NOTE: We use the label `idea` to save the user's requirement and get the content by visiting `content` field.
                # NOTE: Use self.rc.memory.get_by_label to get all memories with this label. Messages are saved in storage in list[Message].
                # NOTE: Use [-1] to get the latest one.
                # NOTE: Use lowercase with `_` to name the label is recommended.
                logger.debug(
                    f"Action {self.rc.todo.name} get {requirement=}"
                )

            except IndexError as e:
                logger.exception(
                    "No user requirement found in memory. Please provide user instruction to query."
                )
                exit(1)
            result = await todo.run(idea=requirement)  # NOTE: Run the action `SimpleWrite` in async.
            logger.info(
                f"Action {self.rc.todo.name} finished. Got the result: {result}"
            )
            # NOTE: Push the result to the memory with the given label
            msg = Message(
                content=result,
                label="code",
                role=self.profile,  # NOTE: Never change this unless you understand what may happen.
                cause_by=type(todo),
                # NOTE: It is recommended not to use any values other than the intended ones for the `caused_by` and `sent_from` fields.
                sent_from=type(todo),
            )
            self.rc.memory.add(msg)  # Use `add` to push the message at the end of the memory list.
        elif self.rc.todo.name == "SimpleCheck":
            try:
                requirement = self.rc.memory.get_by_label("idea")[
                    -1].content  # To get the latest one
                logger.debug(
                    f"Action {self.rc.todo.name} get {requirement=}"
                )
                code = self.rc.memory.get_by_label("code")[-1].content
                logger.debug(f"Action {self.rc.todo.name} get {code=}")

            except IndexError as e:
                logger.exception(
                    "No code or idea found in memory. Please provide them to query."
                )
                exit(1)
            result = await todo.run(code=code, idea=requirement)
            logger.info(
                f"Action {self.rc.todo.name} finished. Got the result: {result}"
            )
            # Push the result to the memory with the given label
            # Try to dump the msg as json model.
            try:
                resp = json.loads(result)
                conclusion = resp["conclusion"]
                issues = resp["issues"]
            except json.decoder.JSONDecodeError as e:
                logger.warning(f"Fail to decode json: {e} in {result=}")
                # We should have retried it but exit here for simplification
                return None
            except Exception as e:
                logger.exception(f"Fail to decode json: {e} in {result=}")
                return None

            msg_conclusion = Message(
                content=conclusion,
                label="conclusion",
                role=self.profile,
                cause_by=type(todo),
                sent_from=type(todo),
            )
            self.rc.memory.add(msg_conclusion)
            if issues is not None:
                msg_issues = Message(
                    content=str(issues),
                    label="issues",
                    role=self.profile,
                    cause_by=type(todo),
                    sent_from=type(todo),
                )
                self.rc.memory.add(msg_issues)
        else:
            # NOTE: Process any unexpected status
            logger.exception(f"Action {self.rc.todo.name} is not implemented or excepted.")
            msg = None
        # NOTE: Use `self.rc.memory.get_all()` to get all memory for debug
        try:
            memories = self.rc.memory.get_all()
            logger.debug(f"Memories:")
            for memory in memories:
                logger.debug(f"{memory.label=},{memory.content=}")
        except Exception as e:
            logger.exception(f"Fail to get memories: {e}")
        return msg if 'msg' in locals() else msg_conclusion

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory)


def main(msg="write a function that calculates the product of a list and run it"):
    idea: str = "write a function that calculates the product of a list and run it"
    team = Team()
    team.hire(
        [CodeWriter()]
    )
    # NOTE: The main entry to build the team and run
    team.invest(investment=100)

    async def run_team(idea_to_run: str):
        """
        Run the AI team project asynchronously.
        """
        # Rewrite it to do the initialization.
        # NOTE: Push the initialization message into a list of tuples in the following format:
        team.run_project(idea_to_run, [("idea", idea_to_run)])
        await team.run(n_round=3)  # NOTE: Define the maximum round to run

    asyncio.run(run_team(idea_to_run=idea))  # Run the team


if __name__ == "__main__":
    define_log_level(print_level="INFO")  # NOTE: Set the log level to INFO
    fire.Fire(main)
