"""dwa"""
import os
import openai
import requests
import os.path
from helper import IMAGE_PATH
from dotenv import load_dotenv
from helper import Character
import itertools
load_dotenv()
APIKEY = os.environ["APIKEY"]
openai.api_key = APIKEY

models = {
    "davinci": "davinci",
    "davinci-003": "text-davinci-003",
}
BASE_KEYWORDS = [
                "\"World of Warcraft\"",
                "Warcraft",
                "Azeroth",
                "Fantasy",
                "Character Creation",
                "Creation",
                "Character Backstory",
                "Character",
                "Backstory",
                "story",
                "DND",
                "\"dungeons and dragons\"",
                "\"dungeons & dragons\""
                ]

def download_image(url:str, character:Character):
    """downloads an image from URL"""
    image_data = requests.get(url, timeout=3).content
    character_name = character.Name.replace(" ", "-")
    with open(f"{os.path.join(IMAGE_PATH,character_name)}.png", "wb") as image_file:
        image_file.write(image_data)
    print(f"saved to {os.path.join(IMAGE_PATH, character.Name.replace(' ','-'))}.png")


def get_keywords(character:Character):
    """
    appends the generated character paramentes to the keywords
    """
    return BASE_KEYWORDS + [character.Presenting_gender,
                            #character.Race_description,
                            character.Class,
                            character.Race,
                            #character.Role,
                            f"{character.Spec} {character.Class}"]

def create_image(image_prompt:str, character:Character):
    """creates an image from the prompt"""
    print("Generating image. Please wait...")
    pre_prompt = f"styles: cartoony, low-detailed, fantasy, portrait. {character.Race}, {character.Class}, {character.Presenting_gender}"
    if len(image_prompt)+(len(pre_prompt)+1) > 1000:
        print(f"old prompt: {image_prompt}")
        print(f"old length: {len(image_prompt)}")
        image_prompt = image_prompt[0:999-(len(pre_prompt)+1)]
        print(f"new prompt: {image_prompt}")
        print(f"new length: {len(image_prompt)}")
        input("enter to continue")
    prompt = f"{pre_prompt} {image_prompt}"
    sizes = {
        "large": "1024x1024",
        "medium": "512x512",
        "small": "256x256",
    }
    resp = openai.Image.create(
        prompt=prompt,
        n=1,
        size=sizes["medium"]
    )
    return resp["data"][0]["url"]

def create_backstory(character:Character):
    """
    creates a backstory for the character based on keywords
    """
    print("generating story. Please wait...")
    image = None
    keywords = get_keywords(character)
    #DEBUG(keywords)
    keywords_prompt = ", ".join(keywords)
    prompt = f"use these keywords for the backstory: {keywords_prompt}. "\
            "the backstory has to be written for the perspectiv of the character. "\
            "The backstory cannot be longer than 255 symbols (letters, spaces, etc...). "\
            "Words such as \"DPS\", \"Tank\" and \"Healer\" refers to the characters role. "\
                "so if DPS, the character is a damage dealer, and so forth. "\
                "so dont say that the character is a DPS, instead say they are " \
                    "\"adept at fighting\" or if its a tank, "\
                    "then they're \"good at protection people\". "\
            "Avoid saying the name \"World of Warcraft\". "\
            "Please note that the world the character lives in is called \"Azeroth\". "\
            "Finish the backstory with the \"END BACKSTORY\". "\
            "create a short character backstory. "\
            "the charaters short description is: "\
            f"I'm {character.Name},"\
                f" a {character.Presenting_gender} {character.Race_description} {character.Class} "
    resp = openai.Completion.create(
        model=models["davinci-003"],
        prompt=prompt,
        max_tokens=256,
        stop=["END BACKSTORY"],
        n=1, # generates n backstories
        temperature=0.7,
    )
    choice = input("generate image[Y/n]: ").lower().strip()
    story = resp.choices[0].text
    if choice == "" or choice == "y":
        image = create_image(story, character)
    if image is not None:
        download_image(image, character)
    return story
