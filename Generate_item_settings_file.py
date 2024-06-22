import argparse
import json
import os
parser = argparse.ArgumentParser()
parser.add_argument("name", nargs = '*')
args = parser.parse_args()
print(args.name[0])
# Load data from JSON files as strings
with open('items.json', 'r') as f:
    all_items = json.load(f)
with open('tempFoods.json', 'w') as f:
    json.dump([i[:3] for i in all_items if i[3] == 'food'], f)
with open('tempDrinks.json', 'w') as f:
    json.dump([i[:3] for i in all_items if i[3] == 'drink'], f)
with open('tempFoods.json', 'r') as f:
    foods_items = f.read()
with open('tempDrinks.json', 'r') as f:
    drinks_items = f.read()
os.remove('tempDrinks.json')
os.remove('tempFoods.json')
# Prepare the data for the file
data_parts = [
    "\n    [Drinks] \n        #Defines items that will recover thirst when drunk': ''\n        #Format': [[\"item-id-1\", \"hydration-amount\", \"quenching-amount\"], [\"item-id-2\", \"hydration-amount\", \"quenching-amount\"]],\n        drinks = ",
    drinks_items,
    "\n    \n    [Foods] \n        #Defines items that will recover thirst when eaten': ''\n        #Format': [[\"item-id-1\", \"hydration-amount\", \"quenching-amount\"], [\"item-id-2\", \"hydration-amount\", \"quenching-amount\"]],\n        foods = ",
    foods_items,
    "\n    \n    [Blacklist] \n        #A mod may have added thirst compatibility to an item via code. If you want to edit the thirst values of that item, add an entry in one of the first two lists. If instead you want to remove thirst support for that item, add an entry in this list': '',\n        #Format': [\"examplemod:example_item_1\", \"examplemod:example_item_2\"],\n        itemsBlacklist= []\n    \n"
]

# Write the data to the file
with open(f'{args.name[0]}.toml', 'w') as f:
    for part in data_parts:
        f.write(part)
