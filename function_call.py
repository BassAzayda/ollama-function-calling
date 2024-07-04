# Importing necessary libraries
import chainlit as cl
import requests
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get current weather


def get_current_weather(location, unit="celsius"):
    """
    Fetches the current weather for a given location.

    Args:
    location (str): The city and country, e.g., "San Francisco, USA"
    unit (str): Temperature unit, either "celsius" or "fahrenheit"

    Returns:
    str: A string describing the current weather, or an error message
    """
    logging.info(f"Getting weather for {location}")
    base_url = "https://api.open-meteo.com/v1/forecast"

    # Set up parameters for the weather API
    params = {
        "latitude": 0,
        "longitude": 0,
        "current_weather": "true",
        "temperature_unit": unit
    }

    # Set up geocoding to convert location name to coordinates
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    location_parts = location.split(',')
    city = location_parts[0].strip()
    country = location_parts[1].strip() if len(location_parts) > 1 else ""

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        # First attempt to get coordinates
        logging.info(f"Fetching coordinates for {location}")
        geo_response = requests.get(geocoding_url, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        logging.debug(f"Geocoding response: {geo_data}")

        # If first attempt fails, try with full location string
        if "results" not in geo_data or not geo_data["results"]:
            geo_params["name"] = location
            geo_response = requests.get(geocoding_url, params=geo_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            logging.debug(f"Second geocoding attempt response: {geo_data}")

        # Extract coordinates if found
        if "results" in geo_data and geo_data["results"]:
            params["latitude"] = geo_data["results"][0]["latitude"]
            params["longitude"] = geo_data["results"][0]["longitude"]
            logging.info(
                f"Coordinates found: {params['latitude']}, {params['longitude']}")
        else:
            logging.warning(f"No results found for location: {location}")
            return f"Sorry, I couldn't find the location: {location}"

        # Fetch weather data using coordinates
        logging.info("Fetching weather data")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        logging.debug(f"Weather data response: {weather_data}")

        # Extract and format weather information
        if "current_weather" in weather_data:
            current_weather = weather_data["current_weather"]
            temp = current_weather["temperature"]
            wind_speed = current_weather["windspeed"]

            result = f"The current weather in {location} is {temp}°{unit.upper()} with a wind speed of {wind_speed} km/h."
            logging.info(f"Weather result: {result}")
            return result
        else:
            logging.warning(f"No current weather data found for {location}")
            return f"Sorry, I couldn't retrieve weather data for {location}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching weather data: {str(e)}")
        return f"An error occurred while fetching weather data: {str(e)}"

# Function to get a random joke


def get_random_joke():
    """
    Fetches a random joke from an API.

    Returns:
    str: A string containing a joke, or an error message
    """
    logging.info("Fetching a random joke")
    joke_url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(joke_url)
        response.raise_for_status()
        joke_data = response.json()
        joke = f"{joke_data['setup']} - {joke_data['punchline']}"
        logging.info(f"Random joke: {joke}")
        return joke
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching joke: {str(e)}")
        return f"An error occurred while fetching a joke: {str(e)}"


# Define tools (functions) that can be called by the AI model
tools = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_random_joke",
        "description": "Get a random joke",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }
]

# Initialize the AI model
model = OllamaFunctions(model="llama3:8b-instruct-q8_0",
                        format="json", temperature=0)
model = model.bind_tools(tools=tools)

# Create the prompt template for the AI model
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(
        content="You are a helpful AI assistant. Use the provided tools when necessary."),
    ("human", "{input}"),
])

# Function to process user queries


def process_query(query):
    """
    Processes user queries by invoking the AI model and calling appropriate functions.

    Args:
    query (str): The user's input query

    Returns:
    str: The response to the user's query
    """
    logging.info(f"Processing query: {query}")
    formatted_prompt = prompt.format_messages(input=query)
    logging.debug(f"Formatted prompt: {formatted_prompt}")
    result = model.invoke(formatted_prompt)
    logging.info(f"Model result: {result}")

    if result.tool_calls:
        for tool_call in result.tool_calls:
            function_name = tool_call['name']
            args = tool_call['args']
            logging.info(f"Function call: {function_name}, Args: {args}")

            if function_name == "get_current_weather":
                return get_current_weather(**args)
            elif function_name == "get_random_joke":
                return get_random_joke()

    return result.content

# Chainlit event handler for chat start


@cl.on_chat_start
async def start():
    """
    Initializes the chat session.
    """
    logging.info("Chat started")
    cl.user_session.set("model", model)

# Chainlit event handler for incoming messages


@cl.on_message
async def main(message: cl.Message):
    """
    Handles incoming user messages, processes them, and sends responses.

    Args:
    message (cl.Message): The incoming user message
    """
    logging.info(f"Received message: {message.content}")
    try:
        response = await cl.make_async(process_query)(message.content)
        logging.info(f"Response: {response}")
        await cl.Message(content=response).send()
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(f"Error: {error_message}")
        await cl.Message(content=error_message).send()
