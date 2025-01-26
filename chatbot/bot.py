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
        self.system_prompt = system_prompt
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({"role": "system", "content": self.system_prompt})


    def __call__(self, user_message: str) -> str:
        """Processes a user message and retrieves a response from the assistant.

        Args:
            user_message (str): The user's input message.

        Returns:
            str: The assistant's response to the input message.
        """
        self.conversation_history.append({"role": "user", "content": user_message})
        response = self.execute()
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def execute(self) -> str:
        """Executes the OpenAI API call using the conversation history.

        Returns:
            str: The assistant's response content.
        """
        print('inside chatbot')
        try:
            if model_config:
                completion = openai.chat.completions.create(
                    model=model_config.get("default_model", "gpt-3.5-turbo"),
                    messages=self.conversation_history,
                    temperature=model_config.get("temperature", 0.1),
                    max_tokens=model_config.get("max_tokens", 300),
                )
            else:
                completion = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.conversation_history,
                )
        except Exception as e:

            raise Exception("Error executing OpenAI API call") from e

        return completion.choices[0].message.content.strip()
    
    def execute_with_loading(self) -> str:
        """Executes the OpenAI API call with a loading indicator."""
        response_received = False

        def loading_message():
            while not response_received:
                print("Generating response...", end="\r", flush=True)
                time.sleep(1)

        # Start the loading message in a separate thread
        loading_thread = threading.Thread(target=loading_message)
        loading_thread.start()

        try:
            response = self.execute()
        finally:
            response_received = True  # Signal the loading thread to stop
            loading_thread.join()  # Ensure the thread stops before proceeding

        return response

