def search_tripadvisor(destination, preferences):
    """
    Action to search TripAdvisor for hotels and activities based on user preferences.

    Parameters:
    - destination (str): The destination where the user is looking to travel.
    - preferences (dict): User preferences (budget, rating, etc.).

    Returns:
    - str: A summary of the best-matching travel options based on the preferences.
    """
    logger.info(
        f"Searching TripAdvisor for {destination} with preferences: {preferences}"
    )

    # Fetch and rank the data
    try:
        ranked_results = fetch_tripadvisor_data(destination, preferences)
    except Exception as e:
        logger.error(f"Error fetching TripAdvisor data: {e}")
        return f"Error fetching TripAdvisor data: {e}"

    # Generate a summary of the top matches
    if not ranked_results:
        logger.warning("No results found that match your preferences.")
        return "No results found that match your preferences."

    # Example summary output
    summary = "Here are the best-matching travel options based on your preferences:\n\n"

    for i, result in enumerate(ranked_results[:5], start=1):  # Top 5 results
        summary += (
            f"{i}. {result['name']} - Rating: {result['rating']}/5\n"
            f"   Price: ${result['price']} per night\n"
            f"   Location: {result['location']}\n"
            f"   Amenities: {', '.join(result['amenities'])}\n\n"
        )

    return summary
