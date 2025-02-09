import logging
from chatbot.config import query_options
from chatbot.utils import process_query, UnknownActionError

logging.basicConfig(
    filename="agent_ai_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    print("AI Travel Planner Chatbot")
    print("Interact with the chatbot to plan your vacation!")

    while True:
        try:
            print("\nYou can:")
            print("- Enter your query directly")
            print("- Choose from these example queries:")
            for option in query_options:
                print(option)
            print("\nTo exit, type 'quit' or press Ctrl+C")

            user_input = input("\nEnter your query or option number (1-4): ").strip()

            if user_input.lower() == "quit":
                print("\nThank you for using AI Travel Planner Chatbot!")
                break

            if user_input in ["1", "2", "3", "4"]:
                user_query = query_options[int(user_input) - 1].split(". ")[1]
            else:
                user_query = user_input

            try:
                result = process_query(user_query)
                print("\nChatbot Response:")
                print(result)
            except ValueError as error:
                print(f"\nError ValueError, main: {error}")
            except UnknownActionError as error:
                print(f"\nUnknown Action Error, main: {error.message}")
            except Exception as error:
                print(f"\nAn unexpected error occurred, main: {error}")

            continue_chat = input(
                "\nWould you like to ask another question? (yes/no): "
            ).lower()
            if continue_chat not in ["yes", "y"]:
                print("\nThank you for using AI Travel Planner Chatbot!")
                break

        except KeyboardInterrupt:
            print("\n\nExiting the program...")
            break


if __name__ == "__main__":
    main()
