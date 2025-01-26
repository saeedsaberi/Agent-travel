def rank_results_by_preferences(data, preferences):
    """
    Rank the results based on user preferences such as budget and rating.

    Parameters:
    - data (list): List of travel options from the API.
    - preferences (dict): The user preferences used to filter the results.

    Returns:
    - list: A list of ranked travel options.
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Ranking {len(data)} travel options based on user preferences.")

    # Filter by budget and rating
    filtered_data = [
        item
        for item in data
        if item["price"] <= preferences["budget"]
        and item["rating"] >= preferences["rating"]
    ]
    logger.debug(
        f"Filtered {len(data) - len(filtered_data)} travel options based on budget and rating."
    )

    # Rank by rating (highest first)
    ranked_data = sorted(filtered_data, key=lambda x: x["rating"], reverse=True)

    return ranked_data

    return preferences
