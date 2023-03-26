"""dadwa"""
try:
    import traceback
    import sys
    from rich import print # pylint: disable=redefined-builtin
    import background
    from helper import Character
    from helper import Pick
    from helper import body_type_to_presenting_gender
    import helper # pylint: disable=ungrouped-imports
except KeyboardInterrupt:
    exit()

EXCEPTION_RAISED = False
picker = Pick()

def display_character(character:Character) -> None:
    """prints character"""
    print(f"your name is {character.Name}, a {character.Presenting_gender} presenting "\
            f"{character.Race_description} {character.Spec} {character.Class}")

def reroll(character:Character):
    """reroll"""
    rerolls = ["everything", "race", "gender", "class", "spec", "name"]
    rerolls.append("main menu")
    print("what do you want to reroll?")
    for i,command in enumerate(rerolls, start=1):
        if command == "everything":
            print(f"{i} [underline]{command.title()}[/underline] [underline][DEFAULT][/underline]")
        else:
            print(f"{i} {command.title()}")

    match input("[REROLL]>>> ").lower().strip():

        case "1" | "everything":
            main(picker.create_character())

        case "2" | "race":
            character.Race = picker.random_race_from_class(character.Class)
            character.Race_description = helper.race_desc(character.Race)
            name_change = input("Change name to a "\
                                f"{character.Race_description} name? [Y/n]: ").lower().strip()
            if  name_change == "y" or name_change == "":
                character.Name = picker.random_name(character.Race, character.Body_type)
            main(character)

        case "3" | "gender":
            character.Body_type = picker.random_body_type()
            character.Presenting_gender = body_type_to_presenting_gender(character.Body_type)
            main(character)

        case "4" | "class":
            character.Class = picker.random_class_from_race(character.Race)
            character.Spec = picker.random_spec(character.Class)[0]
            main(character)

        case "5" | "spec":
            character.Spec = picker.random_spec(character.Class)
            main(character)

        case "6" | "name":
            character.Name = picker.random_name(character.Race, character.Body_type)
            main(character)

        case "7" | "main menu" | "main" | "menu":
            main(character)

        case _: # DEFAULT
            main(picker.create_character())

def main(character:Character=None):
    """main"""
    if character is None:
        print("generating your character")
        character = picker.create_character()

    commands = ["backstory","reroll", "quit"]
    helper.DEBUG(character)

    display_character(character)
    for i,command in enumerate(commands, start=1):
        if command == "backstory":
            print(f"{i}: [underline]{command}[/underline] [underline][DEFAULT][/underline]")
        else:
            print(f"{i}: {command.title()}")
    user_command = input("[MAIN MENU]>>> ").lower().strip()
    match user_command:
        case "1" | "backstory":
            print(background.create_backstory(character))
        case "2" | "reroll":
            reroll(character)
        case "3" | "quit" | "exit" | "q":
            print("exiting...")
            sys.exit()
        case _: # DEFAULT
            print(background.create_backstory(character))

try:
    main()

except Exception as e: # pylint: disable=broad-exception-caught
    EXCEPTION_RAISED = True
    print("unexpected error")
    if EXCEPTION_RAISED:
        TB = traceback.format_exc()
        lines = TB.strip().split("\n")
        print(lines[0:10])
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
