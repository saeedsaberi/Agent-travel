import openai, time
import threading
from .config import api_config
openai.api_key = api_config["OPENAI_API_KEY"]
from chatbot.config import model_config

class ChatBot:
    """A class to interact with OpenAI's chat models while maintaining conversational context."""

    def __init__(self, system_prompt: str = ""):
        """Initializes the ChatBot with a system prompt and model configuration.

        Args:
            system_prompt (str): A system prompt to define the assistant's role. Defaults to an empty string.
            model_config (dict): A dictionary containing the model configuration. Defaults to model_config.
        """
        print("Initializing ChatBot")
        self.system_prompt = system_prompt
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({"role": "system", "content": self.system_prompt})
        print(f"System prompt set: {self.system_prompt}")

    def __call__(self, user_message: str) -> str:
        """Processes a user message and retrieves a response from the assistant.

        Args:
            user_message (str): The user's input message.

        Returns:
            str: The assistant's response to the input message.
        """
        print(f"User message received: {user_message}")
        self.conversation_history.append({"role": "user", "content": user_message})
        response = self.execute()
        self.conversation_history.append({"role": "assistant", "content": response})
        print(f"Assistant response: {response}")
        return response

    def execute(self) -> str:
        """Executes the OpenAI API call using the conversation history.

        Returns:
            str: The assistant's response content.
        """
        print("Executing OpenAI API call")
        try:
            if model_config:
                print("Using model configuration")
                completion = openai.chat.completions.create(
                    model=model_config.get("default_model", "gpt-3.5-turbo"),
                    messages=self.conversation_history,
                    temperature=model_config.get("temperature", 0.1),
                    max_tokens=model_config.get("max_tokens", 300),
                )
            else:
                print("Using default model configuration")
                completion = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.conversation_history,
                )
            print("OpenAI API call successful")
        except Exception as e:
            print(f"Error executing OpenAI API call: {e}")
            raise Exception("Error executing OpenAI API call") from e

        response_content = completion.choices[0].message.content.strip()
        print(f"Response content: {response_content}")
        return response_content

    def execute_with_loading(self) -> str:
        """Executes the OpenAI API call with a loading indicator."""
        print("Starting execute_with_loading")
        response_received = False

        def loading_message():
            print("Loading message thread started")
            while not response_received:
                print("Generating response...", end="\r", flush=True)
                time.sleep(1)
            print("Loading message thread ending")

        # Start the loading message in a separate thread
        print("Starting loading thread")
        loading_thread = threading.Thread(target=loading_message)
        loading_thread.start()

        try:
            print("Calling execute")
            response = self.execute()
            print("Received response")
        finally:
            response_received = True  # Signal the loading thread to stop
            loading_thread.join()  # Ensure the thread stops before proceeding
            print("Loading thread joined")
        return response

