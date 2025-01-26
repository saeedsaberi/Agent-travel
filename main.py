import logging
import streamlit as st

from actions_def.check_query_relevance import check_query_relevance
from actions_def.populate_preferences import populate_preferences
from actions_def.query_with_prepopulated_preferences import search_flights_with_prepopulated_preferences
from actions_def.define_actions import action_re, known_actions
from chatbot.bot import ChatBot
from chatbot.config import api_config, other_params, system_prompt
import openai
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
def process_query(question: str, max_turns: int = 5) -> str:
    """
    Executes a chatbot query to answer a given question.

    Args:
        question (str): The question to be answered.
        max_turns (int, optional): The maximum number of turns allowed for the query. Defaults to 5.

    Returns:
        str: The answer to the question.

    Raises:
        UnknownActionError: If the bot encounters an unknown action.
    """
    if not check_query_relevance(question):
        raise ValueError("Query is not relevant to vacation planning or flight searches.")

    preferences = populate_preferences(question)
    print("preferences", preferences)
    next_prompt =system_prompt + f"""
            The previous history of interactions is: querry: {question}, preferences gathered from the user: {preferences}, then
        """
    bot = ChatBot(system_prompt = next_prompt)
    for _ in range(max_turns):
        result = bot(next_prompt)
        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]

        if actions and actions[0]:
            action, action_input = actions[0].groups()

            if action not in known_actions:
                raise UnknownActionError(action, action_input)

            if action == "search_flights":
                preferences = search_flights_with_prepopulated_preferences(question, preferences)
                
            elif action == "search_internet":
                observation = known_actions[action](action_input)
                next_prompt = f"""
                    The previous history of interactions is: {next_prompt}, then
                    Action: {action} performed, resulting in Observation: {observation},
                """
            else:
                observation = known_actions[action](action_input)
                next_prompt = f"""
                    The previous history of interactions is: {next_prompt}, then
                    Action: {action} performed, resulting in Observation: {observation},
                """

    return next_prompt

# Streamlit GUI setup
def main():
    st.title("AI Travel Planner Chatbot")
    st.write("Interact with the chatbot to plan your vacation!")

    # Options for the user
    options = [
        "I want to book a flight.",
        "I want a hotel with a pool.",
        "Help me find vacation packages.",
        "Custom query"
    ]

    selected_option = st.selectbox("Choose an option or type your query below:", options)

    # If custom query, allow user to input their own text
    if selected_option == "Custom query":
        user_query = st.text_input("Enter your custom query:", "")
    else:
        user_query = selected_option

    # Submit button
    if st.button("Submit Query"):
        if user_query:
            try:
                result = process_query(user_query)
                st.success("Chatbot Response:")
                st.write(result)
            except ValueError as e:
                st.error(f"Error: {e}")
            except UnknownActionError as e:
                st.error(f"Unknown Action Error: {e.message}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a query to proceed.")

# Run the app
if __name__ == "__main__":
    main()