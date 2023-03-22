"""HELPER MODULE"""
import csv
import random
from pathlib import Path
from rich import print # pylint: disable=redefined-builtin
import os.path
from typing import Tuple
import inspect
from dataclasses import dataclass
import name_generator

DATA_PATH = Path("data")
RACE_CLASS_PATH = os.path.join(DATA_PATH, "race_class.csv")
CLASSES_PATH = os.path.join(DATA_PATH, "classes.csv")

@dataclass
class Character:
    """Represents a character"""
    Race:str=None
    Race_description:str=None
    Clan:str=None
    Presenting_gender:str=None
    Body_type:str=None
    Class:str=None

def race_desc(race:str):
    race_descriptors = {
        "dracthyr": "Dracthyrian",
        "human": "Human",
        "dwarf": "Dwarven",
        "elf": "Elven",
        "gnome": "Gnomish",
        "draenei": "Draenic",
        "worgen": "Worgen",
        "orc": "Orcish",
        "tauren": "Tauren",
        "troll": "Trollic",
        "goblin": "Goblin",
        "pandaren": "Pandaren",
        "vulpera": "Vulperan",
        "forsaken": "Forsaken",
        "mechagnome": "Mechagnomish",
        "nightborne": "nightborne",
    }
    split_race = race.split(" ")
    return race_descriptors[split_race[-1].lower()]

def DEBUG(msg):
    frame = inspect.currentframe().f_back
    filename = inspect.getframeinfo(frame).filename
    line_number = inspect.getframeinfo(frame).lineno 
    print(f"[red underline][DEBUG:{filename.split('/')[-1]}:{line_number}][/red underline] {msg}")

def race_class():
    """dada"""
    with open(RACE_CLASS_PATH, "r", encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {}
        for row in reader:
            race = row['race']
            classes = row['class'].split(',')
            data[race] = classes
    return data

def url_safe_name(string:str):
    """makes a string usable to the name generator"""
    return string.replace(" ", "-")

def body_type_to_presenting_gender(body_type:str):
    """returns a presenting gender based on body type"""
    gender_presentations = {
            "1": "male",
            "2": "female"
        }
    return gender_presentations.get(body_type, "female")

class Pick:
    """pick class"""
    def __init__(self) -> None:
        self.race_class = race_class()
        self.body_types = ["1","2"]
        self.gender_presentations = {
            "1": "male",
            "2": "female"
        }
        with open(CLASSES_PATH, "r", encoding="utf8") as __classes_file:
            self.classes = __classes_file.read().splitlines()

    def random_race(self):
        """returns a random race"""
        return random.choice(list(self.race_class.keys()))

    def random_class(self, __true_rng__=True):
        """returns a random  class"""
        if __true_rng__:
            return random.choice(self.classes)
        race = self.random_race()
        return random.choice(self.race_class[race])

    def random_body_type(self):
        """Returns a random body type"""
        return random.choice(self.body_types)

    def random_name(self, race:str, body_type:str):
        """returns a random name based on race and body type"""
        return random.choice(name_generator.get_names(race, body_type))

    def random_race_class(self) -> Tuple[str,str]:
        """returns a valid race/class combo"""
        return (
                race := self.random_race(), # race
                random.choice(self.race_class[race]) # class
                # doing it like this instead of pulling directly from classes file because
                # class/race combo might not be valid unless i pull directly from the 
                # class list within the race itself from the race/class dict
                )

    def random_race_class_body(self) -> Tuple[str,str,str]:
        """returns a random valid race,class & body type"""
        return (*self.random_race_class(), self.random_body_type())

    def create_character(self) -> Character:
        _race,_class = self.random_race_class()
        _body_type = self.random_body_type()
        _presenting_gender = body_type_to_presenting_gender(_body_type)
        _race_desc = race_desc(_race)
        _clan = None
        if len(_race.split(" ")) > 1:
            _clan = " ".join(_race.split(" ")[:-1])
            _race_desc = f"{_clan} {_race_desc}"
        return Character(Race=_race, Race_description=_race_desc, Presenting_gender=_presenting_gender, Body_type=_body_type, Class=_class, Clan=_clan)
