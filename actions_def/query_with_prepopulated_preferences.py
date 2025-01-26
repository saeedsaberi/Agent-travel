import logging


def search_flights_with_prepopulated_preferences(query, preferences):
    """
    Action to query and prepopulate user preferences using a lightweight model, filling in missing info with ask_user.

    Parameters:
    - query (str): The user's input query.

    Returns:
    - dict: The final preferences dictionary after prepopulation and user input.
    """
    logging.info(f"Processing query: {query}")
    # Check if the query is relevant
    if check_query_relevance(query):
        logging.info("Query is relevant. Proceeding with prepopulating preferences.")
        # Prepopulate preferences, ask user for any missing values
        preferences = prepopulate_preferences(query)
        logging.info(f"Prepopulated preferences: {preferences}")

        # Proceed with the vacation planning or flight search using the preferences
        logging.info("Proceeding with the search...")
        # Example: Call the search action (e.g., flights or hotels)
        result = known_actions["search_tripadvisor"](
            query, preferences
        )  # Replace with appropriate action
        logging.info(f"Search result: {result}")
        return preferences

    else:
        logging.info("Query is not relevant to vacation planning or flight searches.")
        return "The query is not relevant to vacation planning or flight searches."
