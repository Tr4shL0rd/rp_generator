"""HELPER MODULE"""
import csv
import random
from pathlib import Path
from typing import Tuple, List
import os.path
import os
import subprocess
import time
import inspect
from dataclasses import dataclass, fields
import psutil
from rich import print # pylint: disable=redefined-builtin
import name_generator

DATA_PATH = Path("data")
RACE_CLASS_PATH = os.path.join(DATA_PATH, "race_class.csv")
CLASSES_PATH = os.path.join(DATA_PATH, "classes.csv")
RACE_PATH = os.path.join(DATA_PATH, "races.txt")
IMAGE_PATH = os.path.join(os.getcwd(), "images")
CURRENT_TIME = time.time()


@dataclass
class Character:
    """Represents a character"""
    Name:str=None
    Race:str=None
    Race_description:str=None
    Clan:str=None
    Presenting_gender:str=None
    Body_type:str=None
    Class:str=None
    Spec:str=None
    Role:str=None
    Edited:Tuple[bool,int,str]=(False,0,"") # changed, times, latest
    Rerolled:Tuple[bool,int,str]=(False,0,"")# changed, times, latest
    Image_model:str=None

def clear_screen():
    """clears the screen"""
    subprocess.call("clear" if os.name == "posix" else "cls", shell=True)

def character_details(character:Character):
    """prints details"""
    for field in fields(character):
        if getattr(character, field.name) is None \
            or \
        isinstance(getattr(character, field.name),bool):

            print(f"[yellow]{field.name}[/yellow]: "\
                    f"[bold pink italic]{getattr(character, field.name)}[/bold pink italic]")
        else:
            print(f"[yellow]{field.name}[/yellow]: [green]{getattr(character, field.name)}[/green]")

def race_desc(race:str):
    """returns the noun of a race"""
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

def DEBUG(msg, **kwargs):
    """DEBUG"""
    frame = inspect.currentframe().f_back
    filename = inspect.getframeinfo(frame).filename
    line_number = inspect.getframeinfo(frame).lineno 
    #if "var_name" in kwargs.keys():
    if kwargs.get("var_name", None) is not None:
        debug_msg = f"[DEBUG:{filename.split('/')[-1]}:{line_number}|{kwargs['var_name']}]"
    else:
        debug_msg = f"[DEBUG:{filename.split('/')[-1]}:{line_number}]"

    print(f"[red underline]{debug_msg}[/red underline] {msg}")

def double_check_firefox_driver_kill():
    """
    double checks if there are any headless firefox processes still running
    """
    for proc in psutil.process_iter(["pid", "name", "create_time"]):
        if proc.info["name"] == "firefox" and CURRENT_TIME - proc.info["create_time"] < 120:
            os.kill(proc.info["pid"], 9)

def race_class():
    """fills the race/class dict"""
    with open(RACE_CLASS_PATH, "r", encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {}
        for row in reader:
            race = row['race']
            classes = row['class'].split(',')
            data[race] = classes
    return data

def body_type_to_presenting_gender(body_type:str):
    """returns a presenting gender based on body type"""
    gender_presentations = {
            "1": "male",
            "2": "female"
        }
    return gender_presentations.get(body_type, "female")

def get_races() -> List[str]:
    """returns a list of all available races"""
    races = []
    with open(RACE_PATH, "r", encoding="utf8") as race_file:
        lines = race_file.readlines()
        for line in lines:
            races.append(line.strip())
    return races

def get_spec_role(character:Character):
    """returns the role of a given spec"""
    spec_role = {
        "Warrior": {
            "Arms": "DPS",
            "Fury": "DPS",
            "Protection": "Tank"
        },
        "Paladin": {
            "Holy": "Healer",
            "Protection": "Tank",
            "Retribution": "DPS"
        },
        "Hunter": {
            "Beast Mastery": "DPS",
            "Marksmanship": "DPS",
            "Survival": "DPS"
        },
        "Rogue": {
            "Assassination": "DPS",
            "Outlaw": "DPS",
            "Subtlety": "DPS"
        },
        "Priest": {
            "Discipline": "Healer",
            "Holy": "Healer",
            "Shadow": "DPS"
        },
        "Death Knight": {
            "Blood": "Tank",
            "Frost": "DPS",
            "Unholy": "DPS"
        },
        "Shaman": {
            "Elemental": "DPS",
            "Enhancement": "DPS",
            "Restoration": "Healer"
        },
        "Mage": {
            "Arcane": "DPS",
            "Fire": "DPS",
            "Frost": "DPS"
        },
        "Warlock": {
            "Affliction": "DPS",
            "Demonology": "DPS",
            "Destruction": "DPS"
        },
        "Monk": {
            "Brewmaster": "Tank",
            "Mistweaver": "Healer",
            "Windwalker": "DPS"
        },
        "Druid": {
            "Balance": "DPS",
            "Feral": "DPS",
            "Guardian": "Tank",
            "Restoration": "Healer"
        },
        "Demon Hunter": {
            "Havoc": "DPS",
            "Vengeance": "Tank"
        }
    }
    return spec_role[character.Class.title()][character.Spec.title()]

def get_current_image_model():
    with open("settings.conf", "r") as f:
        return f.readline().split("=")[-1].replace("\"", "")

def get_class_specs(character:Character):
    """returns spec for class"""
    class_specs = {
            "Death Knight": [("Blood", "Tank"), ("Frost", "DPS"), ("Unholy", "DPS")],
            "Demon Hunter": [("Havoc", "DPS"), ("Vengeance", "Tank")],
            "Druid": [("Balance", "DPS"), ("Feral", "DPS"), ("Guardian", "Tank"), 
                        ("Restoration", "Healer")],
            "Hunter": [("Beast Mastery", "DPS"), ("Marksmanship", "DPS"), ("Survival", "DPS")],
            "Mage": [("Arcane", "DPS"), ("Fire", "DPS"), ("Frost", "DPS")],
            "Monk": [("Brewmaster", "Tank"), ("Mistweaver", "Healer"), ("Windwalker", "DPS")],
            "Paladin": [("Holy", "Healer"), ("Protection", "Tank"), ("Retribution", "DPS")],
            "Priest": [("Discipline", "Healer"), ("Holy", "Healer"), ("Shadow", "DPS")],
            "Rogue": [("Assassination", "DPS"), ("Outlaw", "DPS"), ("Subtlety", "DPS")],
            "Shaman": [("Elemental", "DPS"), ("Enhancement", "DPS"), ("Restoration", "Healer")],
            "Warlock": [("Affliction", "DPS"), ("Demonology", "DPS"), ("Destruction", "DPS")],
            "Warrior": [("Arms", "DPS"), ("Fury", "DPS"), ("Protection", "Tank")],
            "Evoker": [("Devastation", "DPS"), ("Preservation", "Healer")]
        }
    selected_class = class_specs[character.Class.title()]
    return [t[0] for t in selected_class]

def get_race_valid_classes(character:str|Character) -> List[str]:
    """returns a list of race-valid classes"""

    if isinstance(character, Character):
        return race_class()[character.Race]
    elif isinstance(character, str):
        return race_class()[character]

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

    def random_spec(self, c_class:str|Character=None) -> Tuple[str, str]:
        """Returns a random spec from a class [class,role]"""
        class_specs = {
            "Death Knight": [("Blood", "Tank"), ("Frost", "DPS"), ("Unholy", "DPS")],
            "Demon Hunter": [("Havoc", "DPS"), ("Vengeance", "Tank")],
            "Druid": [("Balance", "DPS"), ("Feral", "DPS"), ("Guardian", "Tank"), 
                        ("Restoration", "Healer")],
            "Hunter": [("Beast Mastery", "DPS"), ("Marksmanship", "DPS"), ("Survival", "DPS")],
            "Mage": [("Arcane", "DPS"), ("Fire", "DPS"), ("Frost", "DPS")],
            "Monk": [("Brewmaster", "Tank"), ("Mistweaver", "Healer"), ("Windwalker", "DPS")],
            "Paladin": [("Holy", "Healer"), ("Protection", "Tank"), ("Retribution", "DPS")],
            "Priest": [("Discipline", "Healer"), ("Holy", "Healer"), ("Shadow", "DPS")],
            "Rogue": [("Assassination", "DPS"), ("Outlaw", "DPS"), ("Subtlety", "DPS")],
            "Shaman": [("Elemental", "DPS"), ("Enhancement", "DPS"), ("Restoration", "Healer")],
            "Warlock": [("Affliction", "DPS"), ("Demonology", "DPS"), ("Destruction", "DPS")],
            "Warrior": [("Arms", "DPS"), ("Fury", "DPS"), ("Protection", "Tank")],
            "Evoker": [("Devastation", "DPS"), ("Preservation", "Healer")]
        }

        if isinstance(c_class, Character):
            spec,role = random.choice(class_specs[c_class.Class.title()])
        else:
            spec,role = random.choice(class_specs[c_class.title()])
        return (spec,role)

    def random_body_type(self):
        """Returns a random body type"""
        return random.choice(self.body_types)

    def random_name(self, race:str=None, body_type:str=None):
        """returns a random name based on race and body type"""
        return random.choice(name_generator.get_names(race, body_type))

    def random_class_from_race(self, race:str) -> str:
        """returns a random race-valid class"""
        return random.choice(self.race_class[race])

    def random_race_from_class(self, _class:str) -> str:
        """returns a random class-valid race"""
        class_race = {
            "demon hunter": ["blood elf", "night elf"],
            "death knight": ["human", "dwarf", "night elf", "gnome", "draenei", "worgen",
                                "pandaren", "orc", "undead", "tauren", "troll",
                                "blood elf", "goblin"],
            "druid":        ["night elf", "tauren", "worgen", "troll", "highmountain tauren",
                                "zandalari troll", "kul tiran"],
            "hunter":       ["human","dwarf", "night elf", "gnome", "draenei", "worgen",
                                "pandaren", "orc", "undead", "tauren", "troll", "blood elf",
                                "goblin", "vulpera", "mag'har orc",
                                "dark iron dwarf", "mechagnome"],
            "mage":         ["human","dwarf", "gnome", "draenei", "worgen", "pandaren",
                                "orc", "undead", "troll", "blood elf", "nightborne",
                                "void elf", "lightforged draenei"],
            "monk":         ["human","dwarf", "night elf", "gnome", "draenei", "pandaren",
                                "orc", "undead", "tauren", "troll", "blood elf"],
            "paladin":      ["human","dwarf", "draenei", "tauren", "blood elf",
                                "lightforged draenei", "dark iron dwarf",
                                "mechagnome", "zandalari troll"],
            "priest":       ["human","dwarf", "night elf", "gnome", "draenei", "worgen",
                                "pandaren", "undead", "troll", "blood elf", "void elf",
                                "lightforged draenei"],
            "rogue":        ["human","dwarf", "night elf", "gnome", "draenei", "worgen",
                                "pandaren", "orc", "undead", "troll", "blood elf", "goblin",
                                "vulpera", "mag'har orc", "dark iron dwarf", "mechagnome"],
            "shaman":       ["dwarf","draenei", "orc", "tauren", "troll", "mag'har orc",
                                "dark iron dwarf", "kul tiran", "zandalari troll"],
            "warlock":      ["human","dwarf", "gnome", "orc", "undead", "troll",
                                "blood elf", "goblin", "void elf"],
            "warrior":      ["human","dwarf", "night elf", "gnome", "draenei", "worgen",
                                "pandaren", "orc", "undead", "tauren", "troll", "blood elf",
                                "vulpera", "mag'har orc", "dark iron dwarf", "mechagnome",
                                "kul tiran"],
            "evoker":       ["dracthyr"]
        }
        return random.choice(class_race[_class.lower()])

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

    def race_valid_clan(self, _race):
        """returns a valid clan from race"""
        clan = " ".join(_race.split(" ")[:-1])
        return clan if len(clan) >=1 else None

    def create_character(self) -> Character:
        """creates a random character"""
        character = Character()
        character.Race, character.Class = self.random_race_class()
        character.Body_type = self.random_body_type()
        character.Presenting_gender = body_type_to_presenting_gender(character.Body_type)
        character.Race_description = race_desc(character.Race)
        character.Spec,character.Role = self.random_spec(character.Class)
        character.Name = random.choice(
            name_generator.get_names(
                race=character.Race,
                body_type=character.Body_type)
            )
        if len(character.Race.split(" ")) > 1:
            character.Clan = self.race_valid_clan(character.Race)
            character.Race_description = f"{character.Clan} {character.Race_description}"
        character.Image_model = get_current_image_model()
        return character
        #return Character(
        #                Name=character.Name,
        #                Race=character.Race,
        #                Race_description=character.Race_description,
        #                Spec=character.Spec,
        #                Role=character.Role,
        #                Presenting_gender=character.Presenting_gender,
        #                Body_type=character.Body_type,
        #                Class=character.Class,
        #                Clan=character.Clan,
        #                )
