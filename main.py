import logging

import openai

from actions import query_with_prepopulated_preferences
from actions.define_actions import ACTION_RE, KNOWN_ACTIONS
from chatbot.bot import ChatBot
from chatbot.config import api_config, other_params, system_prompt

openai.api_key = api_config["OPENAI_API_KEY"]

logging.basicConfig(
    filename="agent_ai_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class UnknownActionError(Exception):
    """Exception raised when the bot encounters an unknown action."""

    def __init__(self, action, action_input):
        self.action = action
        self.action_input = action_input
        self.message = f"Unknown action: {action} with input: {action_input}"
        super().__init__(self.message)


def query(question, preferences=None, max_turns=other_params["max_turns"]):
    """
    Executes a chatbot query to answer a given question.

    Args:
        question (str): The question to be answered.
        max_turns (int, optional): The maximum number of turns allowed for the query. Defaults to 5.

    Returns:
        str: The answer to the question.

    Raises:
        Exception: If the bot encounters an unknown action.

    """
    bot = ChatBot(system=system_prompt)
    next_prompt = question
    i = 0

    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        actions = [ACTION_RE.match(a) for a in result.split("\n") if ACTION_RE.match(a)]
        if actions:
            action, action_input = actions[0].groups()
            if action not in KNOWN_ACTIONS:
                logging.error(f"Unknown action: {action} with input: {action_input}")
                raise UnknownActionError(action, action_input)
            elif action == "search_flights":
                preferences = query_with_prepopulated_preferences(question, preferences)
            elif action == "search_internet":
                observation = KNOWN_ACTIONS[action](question, action_input)
            else:
                observation = KNOWN_ACTIONS[action](action_input)

            next_prompt = f"""{action} performed, resulting in Observation: {observation},
                                next_prompt: {next_prompt}
                                """
            logging.info(action)

        else:
            logging.info(result)

            return result


if __name__ == "__main__":
    question = "I want to book a flight to Paris and stay in a hotel with a pool."
    try:
        result = query(question)
        print(result)
    except UnknownActionError as e:
        logging.error(e)
