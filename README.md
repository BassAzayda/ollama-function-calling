# Ollama Function Calling Example

This project demonstrates the power of Ollama Function Calling using a simple chatbot built with Chainlit. The bot can provide current weather information and fetch random jokes, showcasing how AI can be used to understand and respond to user queries.

Unlike dedicated Mistral v0.3, this implementation works with various models and utilizes the experimental OllamaFunction from Langchain. This approach is highly adaptable and can be extended to many other tools and use cases, limited only by your imagination.

## Features

- **Weather Information**: Get real-time weather data for any location worldwide.
- **Random Jokes**: Fetch and display random jokes on demand.
- **AI-Powered Responses**: Utilizes AI to understand user queries and provide appropriate responses.
- **Extensible Framework**: The underlying structure can be adapted for various other functions and tools.

## Requirements

- Python 3.7+
- Ollama installed and running on your system
- Internet connection for API access

## Installation

1. Clone this repository or download the `function_call.py` file:
   ```
   git clone https://github.com/yourusername/ollama-function-calling-example.git
   cd ollama-function-calling-example
   ```

2. Create a `requirements.txt` file in the project directory with the following content:
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

4. Ensure Ollama is installed and running on your system. For installation instructions, please refer to the [Ollama documentation](https://github.com/jmorganca/ollama).

## Usage

1. Start the bot:
   ```
   chainlit run function_call.py
   ```

2. Open your web browser and navigate to `http://localhost:8000`.

3. Interact with the bot through the chat interface. You can ask for weather information, request jokes, or try other queries to test the AI's understanding.

## Examples

Here are some sample queries you can try:

- "What's the current weather in New York?"
- "Tell me a joke"
- "How's the temperature in Tokyo right now?"
- "What's the forecast for London tomorrow?"
- "Give me a funny joke about programming"

Feel free to experiment with different phrasings and requests to explore the AI's capabilities.

## How It Works

1. **User Input**: The user sends a message through the Chainlit interface.
2. **AI Processing**: The Ollama model, utilizing Langchain's OllamaFunction, processes the input to understand the user's intent.
3. **Function Calling**: Based on the understood intent, the appropriate function (weather or joke) is called.
4. **API Interaction**: The chosen function interacts with the respective API (Open-Meteo for weather, Official Joke API for jokes).
5. **Response Generation**: The AI generates a human-readable response based on the API data.
6. **Output**: The response is displayed to the user through the Chainlit interface.

## APIs Used

- **Weather Data**: [Open-Meteo API](https://open-meteo.com/)
- **Jokes**: [Official Joke API](https://official-joke-api.appspot.com/)

No API keys are required for these services, making the setup process straightforward.

## Extending the Project

This example can be extended in numerous ways:

1. Add more functions to handle different types of queries (e.g., news headlines, currency conversion).
2. Integrate with other APIs to expand the bot's knowledge base.
3. Implement more complex conversation flows or multi-turn dialogues.
4. Experiment with different Ollama models to compare performance and capabilities.

## Troubleshooting

- If you encounter any issues with Ollama, ensure it's properly installed and running on your system.
- Check your internet connection if the bot fails to fetch weather data or jokes.
- For any Python package-related issues, try creating a new virtual environment and reinstalling the requirements.

## Contributing

Contributions to improve and extend this example are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

- Thanks to the Ollama team for providing the underlying AI technology.
- Appreciation to Langchain for the experimental OllamaFunction implementation.
- Gratitude to the creators of Chainlit for the user-friendly chat interface.
