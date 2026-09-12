# sourcery skip: do-not-use-staticmethod
"""
A module that contains the AIConfig class object that contains the configuration
"""
from __future__ import annotations

import os
from typing import Type
import yaml


class AIConfig:
    """
    A class object that contains the configuration information for the AI

    Attributes:
        ai_name (str): The name of the AI.
        ai_role (str): The description of the AI's role.
        ai_goals (list): The list of objectives the AI is supposed to complete.
        ai_constraints (list): Extra hard constraints for this preset.
        ai_language (str): Preferred user-facing language (e.g. "English").
        prompt_preamble (str): Optional override for the default independence preamble.
        operating_rules (list): Ordered methods / SOPs the agent should follow.
    """

    def __init__(
        self,
        ai_name: str = "",
        ai_role: str = "",
        ai_goals: list | None = None,
        ai_constraints: list | None = None,
        ai_language: str = "",
        prompt_preamble: str = "",
        operating_rules: list | None = None,
    ) -> None:
        """
        Initialize a class instance

        Parameters:
            ai_name (str): The name of the AI.
            ai_role (str): The description of the AI's role.
            ai_goals (list): The list of objectives the AI is supposed to complete.
            ai_constraints (list): Extra hard constraints for this preset.
            ai_language (str): Preferred user-facing language.
            prompt_preamble (str): Optional override for the default preamble.
            operating_rules (list): Ordered methods / SOPs for this preset.
        Returns:
            None
        """
        if ai_goals is None:
            ai_goals = []
        if ai_constraints is None:
            ai_constraints = []
        if operating_rules is None:
            operating_rules = []
        self.ai_name = ai_name
        self.ai_role = ai_role
        self.ai_goals = ai_goals
        self.ai_constraints = ai_constraints
        self.ai_language = ai_language
        self.prompt_preamble = prompt_preamble
        self.operating_rules = operating_rules

    # Soon this will go in a folder where it remembers more stuff about the run(s)
    SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "ai_settings.yaml")

    @staticmethod
    def load(config_file: str = SAVE_FILE) -> "AIConfig":
        """
        Returns class object with parameters (ai_name, ai_role, ai_goals) loaded from
          yaml file if yaml file exists,
        else returns class with no parameters.

        Parameters:
           config_file (int): The path to the config yaml file.
             DEFAULT: "../ai_settings.yaml"

        Returns:
            cls (object): An instance of given cls object
        """

        try:
            with open(config_file, encoding="utf-8") as file:
                config_params = yaml.load(file, Loader=yaml.FullLoader) or {}
        except FileNotFoundError:
            config_params = {}

        ai_name = config_params.get("ai_name", "")
        ai_role = config_params.get("ai_role", "")
        ai_goals = config_params.get("ai_goals", [])
        ai_constraints = config_params.get("ai_constraints", [])
        ai_language = config_params.get("ai_language", "")
        prompt_preamble = config_params.get("prompt_preamble", "")
        operating_rules = config_params.get("operating_rules", [])
        # type: Type[AIConfig]
        return AIConfig(
            ai_name,
            ai_role,
            ai_goals,
            ai_constraints,
            ai_language,
            prompt_preamble,
            operating_rules,
        )

    def save(self, config_file: str = SAVE_FILE) -> None:
        """
        Saves the class parameters to the specified file yaml file path as a yaml file.

        Parameters:
            config_file(str): The path to the config yaml file.
              DEFAULT: "../ai_settings.yaml"

        Returns:
            None
        """

        config = {
            "ai_name": self.ai_name,
            "ai_role": self.ai_role,
            "ai_goals": self.ai_goals,
        }
        if self.ai_constraints:
            config["ai_constraints"] = self.ai_constraints
        if self.ai_language:
            config["ai_language"] = self.ai_language
        if self.prompt_preamble:
            config["prompt_preamble"] = self.prompt_preamble
        if self.operating_rules:
            config["operating_rules"] = self.operating_rules
        with open(config_file, "w", encoding="utf-8") as file:
            yaml.dump(config, file, allow_unicode=True)

    def construct_full_prompt(self) -> str:
        """
        Returns a prompt to the user with the class information in an organized fashion.

        Parameters:
            None

        Returns:
            full_prompt (str): A string containing the initial prompt for the user
              including the ai_name, ai_role and ai_goals.
        """

        prompt_start = self.prompt_preamble or (
            "Your decisions must always be made independently without"
            " seeking user assistance. Play to your strengths as an LLM and pursue"
            " simple strategies with no legal complications."
        )

        from autogpt.prompt import get_prompt

        # Construct full prompt
        full_prompt = (
            f"You are {self.ai_name}, {self.ai_role}\n{prompt_start}\n\nGOALS:\n\n"
        )
        for i, goal in enumerate(self.ai_goals):
            full_prompt += f"{i+1}. {goal}\n"

        if self.operating_rules:
            full_prompt += "\nOPERATING RULES:\n\n"
            for i, rule in enumerate(self.operating_rules):
                full_prompt += f"{i+1}. {rule}\n"

        if self.ai_constraints:
            full_prompt += "\nPRESET CONSTRAINTS:\n\n"
            for i, constraint in enumerate(self.ai_constraints):
                full_prompt += f"{i+1}. {constraint}\n"

        if self.ai_language:
            full_prompt += (
                f"\nLANGUAGE: All user-facing output, files, and summaries must be in"
                f" {self.ai_language}. Ignore any conflicting language defaults.\n"
            )

        full_prompt += f"\n\n{get_prompt()}"
        return full_prompt
