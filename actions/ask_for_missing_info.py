import logging

from . import ask_user


def ask_for_missing_info(preferences):
    """
    Loop through the preferences and ask the user for missing information.

    Parameters:
    - preferences (dict): The partially prepopulated preferences.

    Returns:
    - dict: The updated preferences dictionary with user-provided values for missing keys.
    """
    questions = {
        "budget": "What's your budget for the trip?",
        "preferred_airports": "Which airport would you prefer to depart from?",
        "flight_time": "What time of the day should the flight be (morning, afternoon, evening)?",
        "rating": "What's the minimum acceptable rating (out of 5)?",
        "accommodation_type": "What type of accommodation are you looking for (e.g., hotel, resort)?",
        "amenities": "Any specific amenities you'd like (e.g., wifi, pool)?",
    }

    logging.info("Asking for missing information")
    # Loop through preferences and ask the user for missing information
    for key, question in questions.items():
        if preferences.get(key) is None:  # Check if the field is missing (None)
            user_input = ask_user(question)
            if key == "amenities":
                # Split amenities into a list if the field is amenities
                preferences[key] = user_input.split(", ")
            else:
                preferences[key] = user_input
            logging.info(f"User provided value for {key}: {preferences[key]}")

    logging.info("Completed asking for missing information")
    return preferences
