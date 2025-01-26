"""
Actions for the chatbot.
"""

import os
import re
import logging
from typing import Any, Callable, Dict
from chatbot.config import SAVE_DIR
from actions_def.ask_user import ask_user
from actions_def.calculate import calculate
from actions_def.generate_schematic_image import generate_schematic_image
from actions_def.populate_preferences import populate_preferences
from actions_def.rank_flights_by_price import rank_flights_by_price
from actions_def.rank_snippets_with_llm import rank_snippets_with_llm
from actions_def.retrieve_and_rank_travel_plans import retrieve_and_rank_travel_plans
from actions_def.search_internet import search_internet
from actions_def.search_flights import search_flights
from actions_def.search_tripadvisor import search_tripadvisor
from actions_def.summarize_with_llm import summarize_with_llm
from actions_def.query_wikipedia import query_wikipedia
from actions_def.rank_travel_plans import rank_travel_plans

# Configure logging
logging.basicConfig(
    filename=os.path.join(SAVE_DIR, "agent_ai_logs.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

known_actions: Dict[str, Callable[..., Any]] = {
    "populate_preferences": populate_preferences,
    "search_tripadvisor": search_tripadvisor,
    "query_wikipedia": query_wikipedia,
    "calculate": calculate,
    "generate_schematic_image": generate_schematic_image,
    "search_internet": search_internet,
    "ask_user": ask_user,
    "search_flights": search_flights,
    "rank_flights_by_price": rank_flights_by_price,
    "retrieve_and_rank_travel_plans": retrieve_and_rank_travel_plans,
    "summarize_with_llm": summarize_with_llm,
    "rank_travel_plans": rank_travel_plans,
    "rank_snippets_with_llm": rank_snippets_with_llm,
}

action_re = re.compile(r"^Action: (\w+): (.*)$")