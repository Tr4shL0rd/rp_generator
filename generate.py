"""dadwa"""
def main():
    picker = helper.Pick()
    character = picker.create_character()

    helper.DEBUG(character)

    helper.DEBUG(f"KEYWORDS: {background.get_keywords(character)}")

    print(f"you're a {character.Presenting_gender} presenting {character.Race_description} {character.Class}")
    print("create backstory[Y/n]? ",end="")
    choice = input("") or "y"
    if choice == "" or choice.lower() == "y":
        print(background.create_backstory(character))

try:
    from rich import print # pylint: disable=redefined-builtin
    import helper
    import background   
    main()
except KeyboardInterrupt:
    print("exiting...")
    import sys
    sys.exit()
