# Pico 2W keyboard
A proyect made by the group Star Dream Sword which allows for the creation of a 5x5 matrix keyboard with an EEPROM for layout storage, leaving the user to modify the layout without requiring to rewrite the source code

# THIS PROJECT IS WIP
This means it hasn't been finished and isn't in a functional state, however the project has the current direction in mind:

## Pico hosted website for layout modification
A huge objective of the project is implementing a GUI capable of leaving you manage the funcionality of each key, this information is to be stored in the EEPROM and should leave one easily modify it without requiring to manage the source code of the project or needing to modify a JSON file

## PCB design upload
This project will mostly make use of a custom made PCB based on the still yet to be uploaded Moonlit Keyboard, a 5x5 version of it along with a slot for a raspberry pico 2W and a space for an 24C16 EEPROM chip

## Key layout storage in EEPROM
Key capabilities are yet to be stablished, it is thought to be either a single key press or a series of them in succession along with the possibility of pressing plenty at the same time, this data should be able to be written into an EEPROM an parsed from it on pico startup, along with an option of writing into it default data if uninitialized
