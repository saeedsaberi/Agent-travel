"""
Pre-populate travel preferences using a lightweight OpenAI model and ask the user for missing info.
"""

import json

import openai

from .ask_for_missing_info import ask_for_missing_info


def prepopulate_preferences(query: str) -> dict:
    """
    Pre-populate travel preferences in JSON format using a lightweight OpenAI model and ask the user for missing info.

    Parameters:
    query (str): The user's input query, typically about vacation preferences or flights.

    Returns:
    dict: A dictionary containing pre-populated preferences, asking the user to fill in any missing values.
    """
    prompt = (
        f"Based on the query '{query}', pre-populate a JSON object containing travel "
        "preferences such as budget, preferred airports, and flight time preferences."
    )

    # Use a lower-size model like 'gpt-3.5-turbo' to infer preferences
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps users plan their vacations.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    # Convert the model output to a dictionary (assuming it returns a valid JSON structure)
    preferences_json = completion.choices[0].message.content
    try:
        preferences = json.loads(preferences_json)
    except json.JSONDecodeError:
        return {}

    # Prepopulate missing fields with null values
    required_fields = [
        "budget",
        "preferred_airports",
        "flight_time",
        "rating",
        "accommodation_type",
        "amenities",
    ]

    for field in required_fields:
        if field not in preferences or preferences[field] is None:
            preferences[field] = None

    # Ask user for missing information
    preferences = ask_for_missing_info(preferences)

    return preferences
