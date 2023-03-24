"""Module for getting names from fantasynamegenerators.com"""
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)


def url_safe_name(string:str):
    """makes a string usable to the name generator"""
    return string.replace(" ", "-")

def click_gender_button(gender:str):
    """clicks a button"""
    gender_buttons = {
        "female": "/html/body/div/div[2]/div/div[4]/div[1]/input[2]",
        "male": "/html/body/div/div[2]/div/div[4]/div[1]/input[1]"
    }
    button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, gender_buttons.get(gender.lower(),"/html/body/div/div[2]/div/div[4]/div[1]/input[2]"))))

    #button = driver.find_element(By.XPATH, gender_buttons.get(gender.lower(),2))
    button.click()

def get_names(race:str, body_type:str):
    """returns names"""
    race = race.lower()
    if race == "mag'har orc":
        race = "orc"
    if not isinstance(body_type, str):
        body_type = str(body_type)
    gender = {
        "1": "male",
        "2": "female"
    }
    special_races = ["dark iron dwarf", "nightborne", "kul tiran human", "mechagnome", "zandalari troll", "lightforged draenei"]
    url = "https://www.fantasynamegenerators.com/"\
            f"{url_safe_name(race).lower()}-wow-names.php"
    if race in special_races:
        if special_races == "kul tiran human":
            url = "https://www.fantasynamegenerators.com/human-wow-names.php"
        else:
            url = "https://www.fantasynamegenerators.com/"\
                    f"wow-{url_safe_name(race).lower()}-names.php"
    driver.get(url)
    # clicks "Get <gender> names" #
    # gendered names doesnt seem to toggle unless pressed twice
    click_gender_button(gender.get(body_type,2))
    click_gender_button(gender.get(body_type,2))

    # Gets names #
    name_container = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "genSection")))
    names_container = WebDriverWait(name_container, 3).until(
        EC.presence_of_element_located((By.ID, "result")))
    names = str(names_container.text) # converting to str for syntax highlight
    driver.quit()
    return random.choice(names.strip().split("\n"))

def quit_driver():
    """
    enables to force the driver to stop from other locations that name_generator.py
    """
    driver.quit()
