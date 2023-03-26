# Project README

This project contains a set of Python modules that generate character names, backstories and descriptions for World of Warcraft players or fantasy RPGs in general. The modules rely on the [OpenAI API](https://openai.com/) for generating backstories, the [selenium library](https://selenium-python.readthedocs.io) for scraping the website [fantasynamegenerators.com](https://www.fantasynamegenerators.com/) to generate names, and the [dotenv library](https://pypi.org/project/python-dotenv/) for securely storing the OpenAI API key.

## Setup

Before running the program, you will need to set up a virtual environment and install the necessary dependencies. To do this, follow these steps:

1. Clone the project repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Create a virtual environment using your preferred method. For example, using [venv](https://docs.python.org/3/library/venv.html), run: `python3 -m venv env`.
4. Activate the virtual environment. For example, run: `source env/bin/activate` on Unix/Linux systems or `.\env\Scripts\activate` on Windows.
5. Install the project dependencies. For example, run: `pip install -r requirements.txt`.

## Obtaining an OpenAI API Key

To use the `background.py` module and generate backstories using the OpenAI API, you will need to obtain an API key. Follow these steps to get your key:

1. Go to the [OpenAI website](https://openai.com/) and sign up for an account.
1. Once you have created an account and logged in, go to the [API Keys page](https://platform.openai.com/account/api-keys).
1. Click the "Generate New Key" button.
1. Give your key a name and select the appropriate permissions for your use case.
1. Click the "Generate Key" button.
1. Copy the generated key and store it securely.

## Adding Your API Key to the Project

To securely store and use your OpenAI API key in the project, you will use the `dotenv` library to create a `.env` file. Follow these steps to add your API key to the project:

1. Create a file named `.env` in the root directory of the project.
1. Add a line to the `.env` file with the key-value pair `APIKEY=your-api-key`, replacing `your-api-key` with your actual API key.
1. Save the `.env` file.

Now, when you run the `background.py` module, it will automatically read the API key from the `.env` file and use it to authenticate with the OpenAI API. Note that the `.env` file should be added to the `.gitignore` file to ensure that it is not accidentally committed to version control.

## Usage

To use the program, run the `generator.py` script in the terminal while the virtual environment is active. The script will generate a character name and ask if you want to create a backstory. If you choose to create a backstory, the script will generate one using the OpenAI API and print it to the console.
Modules

### generator.py

This module contains the main function that generates a character name and backstory. It uses the `helper.py` module to generate a character and the `background.py` module to create a backstory using the OpenAI API.

### background.py

This module contains functions that use the OpenAI API to create a backstory for a character. It also defines a set of base keywords that are used to generate the backstory.

### helper.py

This module contains functions that generate a character name and description by scraping the website [fantasynamegenerators.com](https://www.fantasynamegenerators.com/). It also defines a `Character` class that represents a generated character.

### name_generator.py

This module defines a set of functions that are used to scrape the website [fantasynamegenerators.com](https://www.fantasynamegenerators.com/) to generate names.

## Exceptions

The program catches and handles exceptions in the `generator.py` script using a try-except block. If an exception is caught, the program prints an error message to the console and logs the traceback to a file named `traceback.log`.
