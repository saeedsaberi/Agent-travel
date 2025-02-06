
import logging, json
from actions_def.check_query_relevance import check_query_relevance
from actions_def.populate_preferences import populate_preferences
from actions_def.query_with_prepopulated_preferences import search_flights_with_prepopulated_preferences
from actions_def.define_actions import known_actions
from chatbot.bot import ChatBot
from chatbot.config import api_config, action_re, system_prompt, querry_options
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
    """
    if not check_query_relevance(question):
        raise ValueError("Query is not relevant to vacation planning or flight searches.")

    preferences = populate_preferences(question)
    print("\nCollected preferences:", json.dumps(preferences, indent=2))
    
    next_prompt = system_prompt + f"""
            The previous history of interactions is: query: {question}, preferences gathered from the user: {preferences}, then
        """
    bot = ChatBot(system_prompt=next_prompt)
    
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
                observation = known_actions[action](question, action_input)
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

def main():
    print("AI Travel Planner Chatbot")
    print("Interact with the chatbot to plan your vacation!")

    while True:
        try:
            print("\nYou can:")
            print("- Enter your query directly")
            print("- Choose from these example queries:")
            for option in querry_options:
                print(option)
            print("\nTo exit, type 'quit' or press Ctrl+C")

            user_input = input("\nEnter your query or option number (1-4): ").strip()

            if user_input.lower() == 'quit':
                print("\nThank you for using AI Travel Planner Chatbot!")
                break

            if user_input in ['1', '2', '3', '4']:
                user_query = querry_options[int(user_input)-1].split('. ')[1]
            else:
                user_query = user_input

            try:
                result = process_query(user_query)
                print("\nChatbot Response:")
                print(result)
            except ValueError as e:
                print(f"\nError: {e}")
            except UnknownActionError as e:
                print(f"\nUnknown Action Error: {e.message}")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")

            continue_chat = input("\nWould you like to ask another question? (yes/no): ").lower()
            if continue_chat != 'yes':
                print("\nThank you for using AI Travel Planner Chatbot!")
                break

        except KeyboardInterrupt:
            print("\n\nExiting the program...")
            break

if __name__ == "__main__":
    main()