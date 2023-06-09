# notes for the script

## TODO

* rewrite to use textual
* add support for multiple games
* allow user choosing class, race, prefered gender, and/or role
* speed up name generation


## EXCEPTIONS

### STABLE DIFFUSION

* timeout error
* queue full

### WEBSOCKETS

* WebSocketConnectionClosedException
## Pricing

| Model   | Price/1k tokens |
|---------|-----------------|
| Davinci | $0.0200         |

| Resolution | Price  |
|------------|--------|
| 1024x1024  | $0.020 |
| 512x512    | $0.018 |
| 256x256    | $0.016 |

## LINKS

* [API Docs](https://platform.openai.com/docs/api-reference/)
* [Text Completion Docs](https://platform.openai.com/docs/api-reference/completions/create)
* [Image Creation Docs](https://platform.openai.com/docs/api-reference/images/create)
* [API Usage](https://platform.openai.com/account/usage)
* [Tokenizer](https://platform.openai.com/tokenizer)

## Servers used

* Outland
* Draenor

## Races

### Alliance

* Human
* Dwarf
* Night elf
* Gnome
* Draenei
* Worgen
* Pandaren
* Dracthyr

#### Allied (Alliance)

* Void Elf
* Lightforged Draenei
* Dark Iron Dwarf
* Kul Tiran
* Mechagnome

### Horde

* Orc
* Undead
* Tauren
* Troll
* Blood Elf
* Goblin
* Pandaren
* Dracthyr

#### Allied (Horde)

* Nightborne
* Highmountain Tauren
* Mag'har Orc
* Zandalari Troll
* Vulpera

### Classes

* Warrior
* Hunter
* Priest
* Mage
* Monk
* Demon Hunter
* Evoker
* Paladin
* Rouge
* Shaman
* Warlock
* Druid
* Death Knight
