import streamlit as st
import json
import logging
import openai
from typing import Dict
from chatbot.config import model_config
from chatbot.config import required_fields
# Mock function for asking user for missing info (replace with actual implementation)
def ask_for_missing_info(preferences: Dict) -> Dict:
    for key, value in preferences.items():
        if value is None:
            preferences[key] = st.text_input(f"Enter your preference for {key}:", "")
    return preferences

def populate_preferences(query: str) -> Dict:
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
    client = openai.OpenAI()

    # Use a lower-size model like 'gpt-3.5-turbo' to infer preferences
    completion = client.chat.completions.create(
        model=model_config.get("default_model", "gpt-3.5-turbo"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps users plan their vacations.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=model_config.get("temperature", 0.0),
        max_tokens=model_config.get("max_tokens", 300),
    )

    # Convert the model output to a dictionary (assuming it returns a valid JSON structure)
    preferences_json = completion.choices[0].message.content.strip()
    try:
        preferences = json.loads(preferences_json)
    except json.JSONDecodeError:
        preferences = {}

    # Prepopulate missing fields with null values

    logging.info(f"Prepopulated preferences: {preferences}")

    for field in required_fields:
        if field not in preferences or preferences[field] is None:
            preferences[field.replace("_", " ")] = None

    # Ask user for missing information
    preferences = ask_for_missing_info(preferences)

    return preferences

def main():
    st.title("Travel Preferences Pre-population")
    st.write("Use this tool to generate and refine your travel preferences for vacation planning.")

    # User query input
    user_query = st.text_input("Enter your travel query:", 
                                "e.g.I want to book a flight to Paris with a budget of $1000.")

    preferences = None
    if st.button("Generate Preferences"):
        if user_query:
            try:
                preferences = populate_preferences(user_query)
            except Exception as e:
                raise ValueError(f"Error populating preferences: {e}")
        else:
            st.warning("Please enter a query to proceed.")
    if preferences:
        st.write("Generated Preferences:")
        st.json(preferences)
        return preferences
    else:
        st.warning("No preferences generated.")

if __name__ == "__main__":
    main()
