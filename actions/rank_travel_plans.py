def rank_travel_plans(travel_options, preferences):
    """
    Rank the travel options based on user preferences.

    Parameters:
    - travel_options (list): A list of 100 travel options.
    - preferences (dict): User preferences for ranking.

    Returns:
    - list: Ranked travel options.
    """
    logger = logging.getLogger(__name__)
    logger.info(
        f"Ranking {len(travel_options)} travel options based on user preferences: {preferences}"
    )

    # Example ranking criteria: price, flight duration, user ratings, proximity to destination
    ranked_options = sorted(
        travel_options,
        key=lambda option: (
            option["price"] <= preferences["budget"],  # Prioritize by budget
            -option[
                "rating"
            ],  # Higher-rated plans come first (use negative for descending order)
            option["flight_duration"],  # Shorter flights rank higher
        ),
    )

    logger.info(f"Ranked travel options: {ranked_options}")

    return ranked_options
