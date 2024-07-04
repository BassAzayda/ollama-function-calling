# Ollama Function Calling Example

This is a simple chatbot built with Chainlit that can provide current weather information and random jokes demonstrating the power of Ollama Function Calling. Unlike dedicated Mistral v0.3 this works with a few different models and uses the experimental OllamaFunction from Langchain.

## Features

- Get current weather for any location
- Fetch random jokes
- Uses AI to understand and respond to user queries

## Requirements

- Python 3.7+
- Ollama installed and running on your system

## Installation

1. Clone this repository or download the `function_call.py` file.

2. Create a `requirements.txt` file in the same directory with the following content:

   ```
   chainlit
   requests
   langchain
   langchain_experimental
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the bot:

   ```
   chainlit run function_call.py
   ```

2. Open your web browser and go to `http://localhost:8000`.

3. Interact with the bot by typing messages in the chat interface. You can ask for weather information or request a joke.

## Examples

- "What's the weather like in New York?"
- "Tell me a joke"
- "How's the temperature in Tokyo?"

## Note

This bot uses the Open-Meteo API for weather data and the Official Joke API for jokes. No API keys are required.

Ollama must be installed and running on your system for this bot to function. For installation instructions, please refer to the [Ollama documentation](https://github.com/jmorganca/ollama).
