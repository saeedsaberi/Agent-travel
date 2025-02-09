# actions/check_query_relevance.py
import logging
from chatbot.bot import ChatBot
def check_query_relevance(query):
    """
    Determines if the given query is relevant to the travel agent program.

    Args:
        query (str): The query string to analyze.

    Returns:
        bool: True if the query is relevant to travel planning, False otherwise.
    """
    print(f"Checking query relevance for query: {query}")
    try:
        chat_bot = ChatBot(
            system_prompt=(
                "You are an assistant for a travel agent program. Determine whether a query is relevant to "
                "travel planning activities such as booking flights, hotels, or vacation planning."
            )
        )
        print("Created chat bot, asking for response...")
        response = chat_bot(f'Query: "{query}"\nRespond with "Relevant" or "False".')
        print(f"Got response: {response}")
    except Exception as error:
        print(f"Failed to determine query relevance: {error}")
        logging.error(f"Failed to determine query relevance: {error}")
        return False

    return response.strip() == "Relevant"

