"""dwa"""
import os
import openai
from dotenv import load_dotenv
from helper import Character
load_dotenv()
APIKEY = os.environ["APIKEY"]
openai.api_key = APIKEY

models = {
    "davinci": "davinci",
    "davinci-003": "text-davinci-003",
}
BASE_KEYWORDS = [
                "\"World of Warcraft\"",
                "Warcraft"
                "Azeroth",
                "Fantasy",
                "Character Creation",
                "Creation",
                "Character Backstory",
                "Character",
                "Backstory",
                "story",
                "DND",
                "dungeons and dragons",
                "dungeons & dragons"
                ]


def get_keywords(character:Character):
    """
    appends the generated character paramentes to the keywords
    """
    return BASE_KEYWORDS + [character.Presenting_gender,
                            character.Race_description,
                            character.Class,
                            character.Race]

def create_backstory(character:Character):
    """
    creates a backstory for the character based on keywords
    """
    keywords = get_keywords(character)
    prompt = f"use these keywords for the backstory: {keywords}. "\
            "the backstory has to be written for the perspectiv of the character. "\
            "The backstory cannot be longer than 255 symbols (letters, spaces, etc...). "\
            "Please note that the world the character lives in is called \"Azeroth\". "\
            "Finish the backstory with the \"END BACKSTORY\". "\
            "create a short character backstory. "\
            "the charaters short description is: "\
            f"i'm a {character.Presenting_gender} {character.Race_description} {character.Class} "
    resp = openai.Completion.create(
        model=models["davinci-003"],
        prompt=prompt,
        max_tokens=256,
        stop=["END BACKSTORY"],
        n=1, # generates 5 completions
        temperature=0.7,
    )
    return resp.choices[0].text
