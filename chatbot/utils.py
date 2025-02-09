import json
from actions_def.check_query_relevance import check_query_relevance
from actions_def.populate_preferences import populate_preferences
from chatbot.config import action_re, system_prompt
from actions_def.define_actions import known_actions
from actions_def.query_with_prepopulated_preferences import (
    search_flights_with_prepopulated_preferences,
)
from .bot import ChatBot


class UnknownActionError(Exception):
    """Exception raised when the bot encounters an unknown action."""

    def __init__(self, action: str, action_input: str):
        """
        Initialize an UnknownActionError.

        Args:
            action (str): The unknown action.
            action_input (str): The input to the action.
        """
        self.action = action
        self.action_input = action_input
        self.message = f"Unknown action: {action} with input: {action_input}"
        super().__init__(self.message)


def process_query(input_query: str, max_turns: int = 5) -> str:
    """
    Executes a chatbot query to answer a given question.
    """
    if not check_query_relevance(input_query):
        raise ValueError(
            "Query is not relevant to vacation planning or flight searches."
        )

    user_preferences = populate_preferences(input_query)

    next_input = (
        system_prompt
        + f"""
            The previous history of interactions is: query: {input_query}, preferences gathered from the user: {user_preferences}, then
        """
    )
    bot = ChatBot(system_prompt=next_input)

    for _ in range(max_turns):
        result = bot(next_input)
        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]

        if actions and actions[0]:
            action, action_input = actions[0].groups()

            if action not in known_actions:
                raise UnknownActionError(action, action_input)

            if action == "search_flights":
                user_preferences = search_flights_with_prepopulated_preferences(
                    input_query, user_preferences
                )
            elif action == "search_internet":
                observation = known_actions[action](input_query, action_input)
                next_input = f"""
                    The previous history of interactions is: {next_input}, then
                    Action: {action} performed, resulting in Observation: {observation},
                """
            else:
                observation = known_actions[action](action_input)
                next_input = f"""
                    The previous history of interactions is: {next_input}, then
                    Action: {action} performed, resulting in Observation: {observation},
                """

    return next_input
