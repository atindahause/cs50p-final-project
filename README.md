<p align="center">
  <img src="assets/images/flashAIcards_Logo.png" alt="flashAIcards" width="300">
</p>


# flashAIcards
#### This is my final project for the CS50 Introduction to Programming With Python course at Harvard Online. 
flashAIcards is a modern approach to flashcards creation using artificial intelligence to obtain the flashcards' contents

## About
The intention to write this project began as I saw one opportunity to use the current trends of AI with content generation, and the ongoing accuracy of the current models to generate flashcards that helps students of a wide array of knowledge areas.


## Project general concepts

### Costs
When I was looking for a unified API platform that acts as a big gateway to access a lot of different Large Language Models (LLMs) from various companies such as OpenAI, Anthropic, Google, and Mistral, I found OpenRouter as it provide a lot of completely free models that costs zero tokens to query.
In this way we don't need to pay a subscription fee to a AI povider and we are almost able to use the models that we want, of course, as long as they are free to use :-)

### Models used
As there are some constrains on the availability of the models available for free at OpenRouter, the model that I used to implement this project is the one that was available at the time of this writing (June, 2026), nvidia/nemotron-nano-9b-v2:free.

### PDF generation
fpdf2 library was the chosen one as it offers feature-rich page formatting and is highly versatile and lightweight. 

### API Key protection
I've used the python-dotenv library to read key-value pairs from a .env file and set them as environment variables, to protect the API key.
A .gitignore file is created with the .env inside it. This way Git knows that this file don't have to be uploaded.

### Overview
The main function runs and the get_ai_response() function is called, it query OpenRouters API and receives raw data. The parse_flashcards() function transforms the API's response into a list and the save_to_pdf() function generates a formatted .PDF file.

## Prerequisites
The following pip-installable libraries are required to run the program and are cited in the requirements.txt file:
```
requests
fpdf2
python-dotenv
pytest
```

## Functions and their logic

### main()
The main function that calls all the other functions.

### get_ai_response()
This function Query the OpenRouter's API and returns raw data.
The prompt that is being used limits the number of flashcards to 3, since there are some constraints regarding OpenRouter's free plan.
The model is selected inside the main function.
The API Key is obfuscated by using the python-dotenv library.

**Input:** Prompt created by the user and passed to the AI model through the OpenRouter's API.

**Output:** The API's raw data is returned using the .json method.

### parse_flashcards()
This function primarily transforms the API's response into a list.
Other text methods are used to clean up the response:
.strip() and .split().

**Input:** The API's raw data.

**Output:** The "cards"" object as list data type.

### save_to_pdf()
This function generates a formatted PDF  with the flashcards acquired from the parse_flashcards function.
The fpdf2 library is used to generate and make some adjustments to the .PDF file.

**Input:** "Cards" object.

**Output:** A .PDF file with 3 questions and answers, formatted as flashcards, that used the user's prompt to generate the contents after querying some AI provider.


## Test functions and their logic
The test functions uses mock response strings, instead of querying OpenRouter. As the API key is protected from the code uploaded to github, there is no need to run a test function that actually calls OpenRouter.


## How to run the program?

1. Install the required libraries (requirements.txt file)
2. Obtain an API from OpenRouter and save it at the .env file
3. Choose one model and change it inside the project.py file, in the line beggining with MODEL = ""
2. Run the program
3. Choose a topic for the flashcards
4. The .PDF file will be created at the same directory that you ran the program
