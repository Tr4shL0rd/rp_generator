"""dadwa"""
EXCEPTION_RAISED = False

def main():
    """main"""
    picker = helper.Pick()
    character = picker.create_character()

    helper.DEBUG(character)

    #helper.DEBUG(f"KEYWORDS: {background.get_keywords(character)}")

    print(f"your name is {character.Name}, a {character.Presenting_gender} presenting "\
            f"{character.Race_description} {character.Spec} {character.Class}")
    print("create backstory[Y/n]? ",end="")
    choice = input("") or "y"
    if choice == "" or choice.lower() == "y":
        print(background.create_backstory(character))

try:
    from rich import print # pylint: disable=redefined-builtin
    import helper
    import background
    import sys
    main()

except Exception as e: # pylint: disable=broad-exception-caught
    import traceback
    print("unexpected error")
    TB = traceback.format_exc()
    lines = TB.strip().split("\n")
    print(lines[0:10])
    print(e)

except KeyboardInterrupt:
    import traceback
    TB = traceback.format_exc()
    lines = TB.strip().split("\n")
    print(lines[0:10])
    print("exiting...")

finally:
    import name_generator
    import sys # pylint: disable=ungrouped-imports
    import helper # pylint: disable=ungrouped-imports
    if EXCEPTION_RAISED:
        with open("traceback.log", "w", encoding="utf8") as traceback_log:
            for line in lines:
                traceback_log.write(f"{line}\n")
    name_generator.quit_driver()
    helper.double_check_firefox_driver_kill()
    sys.exit()
