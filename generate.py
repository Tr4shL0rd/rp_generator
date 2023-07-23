"""dadwa"""
try:
    import time
    import traceback
    import sys
    from rich import print # pylint: disable=redefined-builtin
    import background
    from helper import Character
    from helper import Pick
    from helper import body_type_to_presenting_gender
    import helper # pylint: disable=ungrouped-imports
    from helper import IMAGE_PATH
    import getpass
except KeyboardInterrupt:
    exit()

EXCEPTION_RAISED = False
picker = Pick()
def display_character(character:Character) -> None:
    """prints character"""
    print(f"your name is [green underline]{character.Name}[/green underline], "\
            f"a [green underline]{character.Presenting_gender}[/green underline] presenting "\
            f"[green underline]{character.Race_description}[/green underline] "\
            f"[green underline]{character.Spec}[/green underline] "\
            f"[green underline]{character.Class}[/green underline]")

def update_reroll_field(character:Character, rerolled_field:str):
    """
    updates character.Rerolled

    PARAMS:
    -------
        * rerolled_field `str`: the name of the field that was rerolled
    """
    return (True, character.Rerolled[1]+1, rerolled_field)

def update_edit_field(character:Character, edited_field:str):
    """
    updates character.Edited

    PARAMS:
    -------
        * edited_field `str`: the name of the field that was edited
    """
    return (True, character.Edited[1]+1, edited_field)

def generate_story(character:Character):
    """prints the backstory"""
    print(background.create_backstory(character))

def edit_race(character:Character):
    """edit race func"""
    # cut into smaller functions
    helper.clear_screen()
    # display races
    races = helper.get_races()
    print("available races")
    for i,race in enumerate(races, start=1):
        if race == character.Race:
            print(f"{i}: [underline]{race.title()}[/underline] [underline](your race)[/underline]")
        else:
            print(f"{i}: {race.title()}")
    print("please select a new race by entering the name or the "\
            f"id[1-{len(races)}] (CURRENTLY ONLY ID)")
    new_race = input("select new race: ").strip().lower()
    if new_race.isnumeric():
        selected_race = races[int(new_race)-1]
    else:
        selected_race = new_race.title()
    if not selected_race:
        print("error: not selected race")
        exit()

    race_choice = input(f"change to {selected_race} [Y/n]: ").lower().strip()
    if race_choice == "n":
        edit_menu(character)
    character.Race = selected_race
    character.Race_description = helper.race_desc(character.Race)
    character.Clan = picker.race_valid_clan(character.Race)

    # change name
    name_choice = input(
                            f"Change name to a {character.Race_description} name[Y/n]: "
                        ).strip().lower()
    if name_choice == "y" or name_choice == "":
        character.Name = picker.random_name(character.Race,character.Body_type)
        print(f"new name: {character.Name}")
    else:
        main_menu(character)

    # change class
    if character.Class not in helper.get_race_valid_classes(character):
        print(f"current class[{character.Class}] "\
                f"is not a valid class for {character.Race}.")
        print("[blue underline]class and spec will be "\
                "changed to a random race-valid class[/blue underline]")
        print("do you want to change[Y/n]?")
        class_choice = input("").strip().lower()
        if class_choice == "n":
            main_menu(character)
        character.Class = picker.random_class_from_race(character.Race)
        character.Spec = picker.random_spec(character)[0]
    main_menu(character)

def edit_class(character:Character, *kwargs):
    """edits the class of the character"""
    # class menu
    helper.clear_screen()

    def class_menu():
        helper.clear_screen()
        classes = helper.get_race_valid_classes(character)
        print(f"available {character.Race} classes")
        for class_id,_class in enumerate(classes,start=1):
            print(f"{class_id}: {_class.title()}")
        chosen_class = input(f"select class[1-{len(classes)}]: ").strip().lower()
        if chosen_class == "back" or chosen_class == "menu" or chosen_class == "main menu":
            main_menu(character)
        if not chosen_class.isalpha():
            if int(chosen_class) < 1 or int(chosen_class) > len(classes):
                print(f"id {chosen_class} not available")
                getpass.getpass(prompt="press \"ENTER\" to continue")
                class_menu()
        else:
            print(f"{chosen_class} not available")
            getpass.getpass(prompt="press \"ENTER\" to continue")
            class_menu()

        character.Class = classes[int(chosen_class)-1]

    def spec_menu():
        """spec menu"""
        class_specs = helper.get_class_specs(character)
        helper.clear_screen()
        print(f"current spec & role: {character.Spec} [{character.Role}]")
        print(f"available {character.Class} specs")
        for spec_id,spec in enumerate(class_specs, start=1):
            print(f"{spec_id}: {spec.title()}")
        chosen_spec = input(f"Select a spec[1-{len(class_specs)}]: ").strip().lower()
        if chosen_spec == "back" or chosen_spec == "menu" or chosen_spec == "main menu":
            main_menu(character)
        try:
            character.Spec  = class_specs[int(chosen_spec)-1]
        except (IndexError, ValueError):
            helper.clear_screen()
            print("please select a valid spec!")
            time.sleep(0.5)
            spec_menu()
        character.Role = helper.get_spec_role(character)
        main_menu(character)
    if "spec" in kwargs:
        spec_menu()
    class_menu()
    spec_menu()

def edit_name(character:Character):
    """edit character name"""
    print(f"your Name: {character.Name}")

    new_name = input("new name: ").lower().strip()
    print(f"rename \"{character.Name.title()}\" to \"{new_name.title()}\" [Y/n]? ",end="")
    choice = input("").lower().strip()
    if choice == "n":
        main_menu(character)
    character.Name = new_name.title()

def reroll(character:Character):
    """reroll"""
    helper.clear_screen()
    rerolls = [
                "everything",
                "race",
                "gender",
                "class",
                "spec",
                "name"
            ]
    rerolls.append("main menu")
    print("what do you want to reroll?")
    for i,command in enumerate(rerolls, start=1):
        if command == "everything":
            print(f"{i} [underline]{command.title()}[/underline] [underline][DEFAULT][/underline]")
        else:
            print(f"{i} {command.title()}")
    user_command = input("[REROLL]>>> ").lower().strip()
    match user_command:

        case "1" | "everything" as match_case:
            character.Rerolled = update_reroll_field(character, rerolls[int(match_case)-1])
            character = picker.create_character()
            main_menu(character)

        case "2" | "race" as match_case:
            character.Rerolled = update_reroll_field(character, rerolls[int(match_case)-1])
            character.Race = picker.random_race_from_class(character.Class)
            character.Race_description = helper.race_desc(character.Race)
            name_change = input("Change name to a "\
                                f"{character.Race_description} name? [Y/n]: ").lower().strip()
            if  name_change == "y" or name_change == "":
                character.Name = picker.random_name(character.Race, character.Body_type)
            main_menu(character)

        case "3" | "gender" as match_case:
            character.Rerolled = update_reroll_field(character, rerolls[int(match_case)-1])
            character.Body_type = picker.random_body_type()
            character.Presenting_gender = body_type_to_presenting_gender(character.Body_type)
            main_menu(character)

        case "4" | "class" as match_case:
            character.Rerolled = update_reroll_field(character, rerolls[int(match_case)-1])
            character.Class = picker.random_class_from_race(character.Race)
            character.Spec = picker.random_spec(character.Class)[0]
            character.Role = picker.random_spec(character.Class)[1]
            main_menu(character)

        case "5" | "spec" as match_case:
            character.Rerolled = update_reroll_field(character, rerolls[int(match_case)-1])
            character.Spec = picker.random_spec(character.Class)[0]
            character.Role = picker.random_spec(character.Class)[1]
            main_menu(character)

        case "6" | "name" as match_case:
            character.Name = picker.random_name(character.Race, character.Body_type)
            character.Rerolled = update_reroll_field(character, rerolls[int(match_case)-1])
            main_menu(character)

        case "7" | "main menu" | "main" | "menu" | "back":
            main_menu(character)

        case _: # DEFAULT
            if user_command == "":
                main_menu(picker.create_character())
            else:
                print("[red underline]Please select a valid menu option[/red underline]")
                time.sleep(0.5)

def edit_menu(character:Character):
    """Edit"""
    helper.clear_screen()
    edits = [
                "name",
                "race",
                "presenting gender",
                "class",
                "spec",
                "Main Menu"
            ]
    print("What do you want to edit?")
    for i,command in enumerate(edits, start=1):
        print(f"{i}: {command.title()}")
    user_command = input("[EDIT MENU]>>> ").lower().strip()
    match user_command:

        case "1" | "name" as match_case:
            character.Edited = update_edit_field(character, edits[int(match_case)-1])
            edit_name(character)
            #main(character)

        case "2" | "race" as match_case:
            character.Edited = update_edit_field(character, edits[int(match_case)-1])
            edit_race(character)
            #main(character)

        case "3" | "presenting gender" | "gender"| "sex" | "body type" as match_case:
            character.Edited = update_edit_field(character, edits[int(match_case)-1])
            # 1 = male
            # 2 = female
            if character.Body_type == "2":
                character.Body_type = "1"

            elif character.Body_type == "1":
                character.Body_type = "2"

            character.Presenting_gender = helper.body_type_to_presenting_gender(character.Body_type)
            #main(character)

        case "4" | "class" as match_case:
            character.Edited = update_edit_field(character, edits[int(match_case)-1])
            print(f"your Class: {character.Class}")
            edit_class(character)

        case "5" | "spec" as match_case:
            character.Edited = update_edit_field(character, edits[int(match_case)-1])
            print(f"your Spec: {character.Spec}")
            edit_class(character, "spec")

        case "6" | "main" | "main menu" | "back":
            main_menu(character)

        case _:
            if user_command == "":
                print("please enter a valid menu entry")
                edit_menu(character)
            else:
                print("[red underline]Please select a valid menu option[/red underline]")
                time.sleep(0.5)
                edit_menu(character)

def backstory_menu(character:Character):
    """backstory menu"""
    helper.clear_screen()
    commands = [
                    "backstory & image",
                    "backstory",
                    "main menu"
                ]
    for i, command in enumerate(commands, start=1):
        if command == "backstory & image":
            print(f"{i}: [underline]{command.title()}[/underline]")
        else:
            print(f"{i}: {command.title()}")

    user_command = input("[BACKSTORY]>>> ").lower().strip()
    match user_command.lower().strip():
        case "1" | "backstory and image" | "backstory & image":
            story = background.create_backstory(character)
            background.create_image(story, character, helper.get_current_image_model())
            print(story)
            main_menu(character)
        case "2" | "backstory":
            print(generate_story(character))
            main_menu(character, "no_clear")

        case "3" | "(main menu" | "back":
            helper.clear_screen()
            main_menu(character, "no_clear")

        case _:
            if user_command == "":
                story = background.create_backstory(character)
                background.create_image(story, character, helper.get_current_image_model())
                print(story)
                main_menu(character, "no_clear")
            else:
                print("[red underline]Please select a valid menu option[/red underline]")
                time.sleep(0.5)
                backstory_menu(character)

def settings_models(character:Character):
    """settings for image generation models"""
    helper.clear_screen()
    models = [
        "stable diffusion",
        "dall-e",
        "main menu"
    ]
    for i, model in enumerate(models, start=1):
        if model == models[0]:
            print(f"{i}: [underline]{model.title()}[/underline] [underline][DEFAULT][/underline]")
        else:
            print(f"{i}: {model.title()}")
    user_command = input("[MODEL SETTINGS]>>> ").lower().strip()
    using_model = ""
    match user_command:
        case "1" | "stable diffusion" | "sd":
            print("use stable diffusion")
            using_model = "stable diffusion"
        case "2" | "dall-e" | "dalle":
            print("use dall-e")
            using_model = "dall-e"
        case "3" | "back" | "main menu":
            main_menu(character)
        case _:
            if user_command == "":
                using_model = "stable diffusion"
            else:
                print("[red underline]Please select a valid menu option[/red underline]")
                time.sleep(0.5)
                settings_menu(character)

    with open("settings.conf", "w", encoding="utf8") as settings_file:
        settings_file.write(f"image_model=\"{using_model}\"")
    main_menu(character)

def settings_menu(character:Character):
    """Settings menu"""
    helper.clear_screen()
    commands = ["image models", "clear image folder", "main menu"]
    for i, command in enumerate(commands,start=1):
        print(f"{i}: {command.title()}")
    user_command = input("[SETTINGS]>>> ").lower().strip()
    match user_command:
        case "1" | "image models" | "models":
            settings_models(character)
        case "2" | "clear image folder" | "image folder" | "clear":
            helper.clear_images()
            main_menu(character)
        case "3" | "back" | "main" | "main menu":
            helper.clear_screen()
            main_menu(character)
        case _:
            print("please select a menu option")
            settings_menu(character)

    
def main_menu(character:Character, *args):
    """main"""
    if helper.get_folder_size(IMAGE_PATH) >= 5 * 10**6:
        helper.clear_images()
    if character is None:
        print("generating your character")
        character = picker.create_character()
    if character.Image_model is None:
        character.Image_model = "stable diffusion"
    if "no_clear" not in args:
        helper.clear_screen()

    commands = [
                    "backstory",
                    "reroll",
                    "edit",
                    "details",
                    "settings",
                ]
    commands.append("quit")
    #helper.DEBUG(character)
    display_character(character)
    for i,command in enumerate(commands, start=1):
        if command == "backstory":
            print(f"{i}: [underline]{command.title()}[/underline] [underline][DEFAULT][/underline]")
        else:
            print(f"{i}: {command.title()}")
    user_command = input("[MAIN MENU]>>> ").lower().strip()
    match user_command:
        case "1" | "backstory":
            backstory_menu(character)
            #generate_story(character)

        case "2" | "reroll":
            reroll(character)

        case "3" | "edit":
            edit_menu(character)

        case "4" | "details":
            helper.clear_screen()
            helper.character_details(character)
            input("press \"ENTER\" to continue")
            main_menu(character)

        case "5" | "settings":
            settings_menu(character)
        case "6" | "quit" | "exit" | "q":
            print("exiting...")
            helper.double_check_firefox_driver_kill()
            sys.exit()

        case _: # DEFAULT
            if user_command == "":
                backstory_menu(character)
            else:
                print("[red underline]Please select a valid menu option[/red underline]")
                time.sleep(0.5)
                main_menu(character)

try:
    main_menu(None)

except Exception as e: # pylint: disable=broad-exception-caught
    EXCEPTION_RAISED = True
    print("unexpected error")
    if EXCEPTION_RAISED:
        TB = traceback.format_exc()
        lines = TB.strip().split("\n")
        print(lines[0:10])
        print(f"exception type: {type(e).__name__}")
        print(e)

except KeyboardInterrupt:
    EXCEPTION_RAISED = True
    if EXCEPTION_RAISED:
        TB = traceback.format_exc()
        lines = TB.strip().split("\n")
        print(lines[0:10])
    print("exiting...")

finally:
    if EXCEPTION_RAISED:
        with open("traceback.log", "w", encoding="utf8") as traceback_log:
            for line in lines:
                traceback_log.write(f"{line}\n")
    helper.double_check_firefox_driver_kill()
    sys.exit()
