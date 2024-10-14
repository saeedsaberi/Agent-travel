import logging


def ask_user(question):
    """
    Ask a clarifying question to the user.

    Parameters:
    - question: str, the question to ask the user.

    Returns:
    - str, the user's response.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Asking user for clarification: {question}")
    user_response = input(f"Clarification needed: {question}\n Your response: ")
    logger.info(f"User response: {user_response}")
    return user_response
