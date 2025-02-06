import json
import logging
import openai
from typing import Dict, Any, Optional
from chatbot.config import model_config, required_fields

def ask_for_missing_info(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ask the user for missing preferences via terminal input with predefined options.
    """
    for field, options in required_fields.items():
        if field not in preferences or preferences[field] is None:
            while True:
                print(f"\nAvailable options for {field}:")
                for idx, option in enumerate(options, 1):
                    print(f"{idx}. {option}")
                
                choice = input(f"Enter number for {field} (1-{len(options)}): ")
                
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(options):
                        preferences[field] = options[choice_idx]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
    
    return preferences

def populate_preferences(query: str) -> Dict[str, Any]:
    """
    Pre-populate travel preferences using OpenAI model and ask for missing info.
    """
    # Create a system prompt that includes the required fields and their options
    system_prompt = "You are an AI assistant that helps users plan their vacations. "
    system_prompt += "Use only the following options for these fields:\n"
    for field, options in required_fields.items():
        system_prompt += f"- {field}: {', '.join(options)}\n"

    user_prompt = (
        f"Based on the query '{query}', create a JSON object with travel preferences. "
        f"Only include fields: {', '.join(required_fields.keys())}. "
        "If a preference isn't clear from the query, set it to null."
    )

    client = openai.OpenAI()
    
    completion = client.chat.completions.create(
        model=model_config.get("default_model", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=model_config.get("temperature", 0.0),
        max_tokens=model_config.get("max_tokens", 300),
    )

    # Parse the model output
    preferences_json = completion.choices[0].message.content.strip()
    try:
        preferences = json.loads(preferences_json)
    except json.JSONDecodeError:
        preferences = {field: None for field in required_fields}

    logging.info(f"Prepopulated preferences: {preferences}")

    # Ensure all required fields are present
    for field in required_fields:
        if field not in preferences:
            preferences[field] = None

    # Ask user for missing information
    preferences = ask_for_missing_info(preferences)

    return preferences