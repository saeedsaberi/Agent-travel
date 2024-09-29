
# AGENTIC AI Project

This project implements an advanced Agentic AI system using OpenAI's API, designed to handle various queries related to vacation planning and travel searches. The AI autonomously performs actions such as querying flight information, searching for hotels, ranking results, and providing recommendations based on user preferences. The project features structured logging to record queries, actions, and results for debugging and further analysis.

## Workflow Overview

The AGENTIC AI system follows a structured workflow to ensure accurate and contextually relevant responses. Below is a simplified explanation of the system's operation:

1. **User Input**: The process begins when the user inputs a travel-related query, such as flight searches or hotel recommendations.

2. **Query Relevance Check**: The system checks if the query is relevant to vacation planning or travel searches. If relevant, it proceeds to prepopulate preferences.

3. **Prepopulate Preferences**: Based on the user's query, the system generates a JSON object with travel preferences like budget, preferred airports, flight time, and accommodation preferences. If any preference data is missing, the system prompts the user to fill in the gaps.

4. **Agentic AI Process**: 
   - The AI analyzes the query and determines which action to take, such as searching for flights or hotels. 
   - It can autonomously decide the best action based on the context of the query and the user's preferences.

5. **Known Actions**:
   - **Search Flights**: The AI uses travel APIs like Google Flights to search for flights based on user preferences such as budget, preferred departure airports, and flight time.
   - **Search Hotels (TripAdvisor)**: The system fetches data from APIs like TripAdvisor to provide hotel recommendations based on user criteria such as budget, rating, and amenities.
   - **Ask User**: If needed, the system prompts the user for clarification or additional preferences.
   - **Search Internet**: The AI fetches relevant information from the web, ranks the snippets, and provides a concise summary.
   - **Generate Schematic**: Uses AI tools to generate schematic images based on detailed descriptions.

6. **Logging**: All actions, queries, and results are logged for reference and debugging. This helps track the AI's decision-making process and the outcome of each action.

7. **Final Response**: After performing the necessary actions, the AI compiles and delivers a final, refined response to the user.

This workflow ensures the AI can handle complex travel-related queries efficiently and provide personalized responses based on user preferences.

## Example Workflow

1. **User Input**: 
    - _"I want to book a flight to Paris and stay in a hotel with a pool."_
2. **Query Relevance Check**:
    - The system identifies the query as relevant to travel and begins processing.
3. **Prepopulate Preferences**:
    - The system generates preferences such as budget, preferred flight time, and preferred airport. Missing information, such as budget, is requested from the user.
4. **Flight and Hotel Search**:
    - The system searches for available flights and hotel options using APIs like Google Flights and TripAdvisor, ranking results based on user preferences.
5. **Final Response**:
    - The AI delivers a list of ranked flight and hotel options, complete with details like pricing and amenities.

### Example Schematic

![Simplified Schematic](./image/schematic_image.png)

The above diagram illustrates how the AI system processes travel-related queries and generates responses based on the user's preferences.

## Installation

1. Clone the repository.
2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables for the API keys (OpenAI, Google Flights, TripAdvisor, etc.):

    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    export TRIPADVISOR_API_KEY='your-tripadvisor-api-key-here'
    ```

## Usage

To start the chatbot, run the `main.py` file:

```bash
python main.py

This will launch the AI system, ready to handle queries related to vacation planning and flight/hotel searches.

# Example Usage

Input a query like:
bash
Copy code
I want to book a flight to New York and stay in a hotel with free WiFi.
The system will process the query, check for relevance, prepopulate preferences, and fetch flight/hotel recommendations based on user preferences.

## Installation

1. Clone the repository.
2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variable for the OpenAI API key:

    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```

## Usage

To start the chatbot, run the `main.py` file:

```bash
python main.py
# Agent-travel
