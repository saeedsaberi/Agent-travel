import logging
from actions_def.ask_user import ask_user

def clarify_missing_preferences(preferences):
    """
    Clarify missing preferences by asking the user appropriate questions.

    Parameters:
        preferences (dict): Current preferences of the user.

    Returns:
        dict: Updated preferences with user input for missing values.
    """
    # Get the list of missing preferences
    missing_preferences = [key for key, value in preferences.items() if not value]

    # Log the number of missing preferences
    logging.info(f"Clarifying {len(missing_preferences)} missing preferences")

    # Loop through the missing preferences and ask the user for input
    for preference in missing_preferences:
        # Construct the question to ask the user
        question = f"Please provide your {preference} preference (e.g., budget, preferred airports, etc.):"

        # Log the question being asked
        logging.info(f"Asking user for {preference} preference")

        # Print the question
        print(question)

        # Ask the user for input
        user_response = ask_user(question)

        # Log the user's response
        logging.info(f"User provided {preference} preference: {user_response}")

        # Print the user's response
        print(f"User provided {preference} preference: {user_response}")

        # Update the preferences dictionary with the user's response
        preferences[preference] = user_response

    # Log that the clarification process is complete
    logging.info("Completed clarifying missing preferences")

    # Print that the clarification process is complete
    print("Completed clarifying missing preferences")

    # Return the updated preferences dictionary
    return preferences

