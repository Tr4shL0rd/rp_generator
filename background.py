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
BASE_KEYWORDS = ["World of Warcraft", "Fantasy", "Character Creation", "Character Backstory", "Backstory"]


def get_keywords(character:Character):
    return BASE_KEYWORDS + [character.Presenting_gender,
                            character.Race_description,
                            character.Class]

def create_backstory(character:Character):
    keywords = get_keywords(character)
    resp = openai.Completion.create(
        model=models["davinci-003"],
        prompt=f"using these keywords: {keywords}. "\
            "create a short character backstory. "\
            "the charaters short description is: "\
            f"i'm a {character.Presenting_gender} {character.Race_description} {character.Class} ",
        max_tokens=256,
        stop=["END BACKSTORY"],
        n=1, # generates 5 completions
        temperature=0.7,
    )
    return resp.choices[0].text
