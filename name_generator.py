"""Module for getting names from fantasynamegenerators.com"""
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def url_safe_name(string:str):
    """makes a string usable to the name generator"""
    return string.replace(" ", "-")

def click_gender_button(driver:WebDriver,gender:str):
    """clicks a button"""
    try:
        gender_buttons = {
            "female": "/html/body/div/div[2]/div/div[4]/div[1]/input[2]",
            "male": "/html/body/div/div[2]/div/div[4]/div[1]/input[1]"
        }
        button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, gender_buttons.get(gender.lower(),"/html/body/div/div[2]/div/div[4]/div[1]/input[2]"))))
        button.click()
    except Exception as _: # pylint:disable=broad-exception-caught
        with open("traceback.log", "a", encoding="utf8") as traceback_log:
            traceback_log.write(f"URL = {driver.current_url}")

def get_names(race:str, body_type:str):
    """returns names"""
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    race = str(race).lower()
    if race == "mag'har orc":
        race = "orc"
    if not isinstance(body_type, str):
        body_type = str(body_type)
    gender = {
        "1": "male",
        "2": "female"
    }
    url = "https://www.fantasynamegenerators.com/"\
            f"{url_safe_name(race).lower()}-wow-names.php"
    special_races = ["dark iron dwarf", "nightborne", "mechagnome",
                        "zandalari troll", "lightforged draenei",
                        "vulpera", "void elf", "highmountain tauren",
                        "kul tiran human"]
    if race.lower() in special_races:
        if race == "kul tiran human":
            url = "https://www.fantasynamegenerators.com/human-wow-names.php"
        else:
            url = "https://www.fantasynamegenerators.com/"\
                    f"wow-{url_safe_name(race).lower()}-names.php"
    driver.get(url)
    # clicks "Get <gender> names" #
    # gendered names doesnt seem to toggle unless pressed twice
    click_gender_button(driver,gender.get(body_type,2))
    click_gender_button(driver,gender.get(body_type,2))

    # Gets names #
    name_container = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "genSection")))
    names_container = WebDriverWait(name_container, 3).until(
        EC.presence_of_element_located((By.ID, "result")))
    names = str(names_container.text) # converting to str for syntax highlight
    driver.quit()
    names = names.strip().split("\n")
    # return random.choice(names)
    # returns the full list because returning a random elem caused
    # problems when rerolling name.
    # the problem was that the new name would only be the first letter of the
    # returned name
    return names
