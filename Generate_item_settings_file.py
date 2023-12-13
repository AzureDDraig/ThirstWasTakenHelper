# Load data from JSON files as strings
with open('drink.json', 'r') as f:
    drinks = f.read()
with open('food.json', 'r') as f:
    foods = f.read()

# Prepare the data for the file
data_parts = [
    "{\n    'Drinks': {\n        '#Defines items that will recover thirst when drunk': '',\n        '#Format': [[\"item-id-1\", \"hydration-amount\", \"quenching-amount\"], [\"item-id-2\", \"hydration-amount\", \"quenching-amount\"]],\n        'items':\n",
    drinks,
    "\n    },\n    'Foods': {\n        '#Defines items that will recover thirst when eaten': '',\n        '#Format': [[\"item-id-1\", \"hydration-amount\", \"quenching-amount\"], [\"item-id-2\", \"hydration-amount\", \"quenching-amount\"]],\n        'items':\n",
    foods,
    "\n    },\n    'Blacklist': {\n        '#A mod may have added thirst compatibility to an item via code. If you want to edit the thirst values of that item, add an entry in one of the first two lists. If instead you want to remove thirst support for that item, add an entry in this list': '',\n        '#Format': [\"examplemod:example_item_1\", \"examplemod:example_item_2\"],\n        'itemsBlacklist': []\n    }\n}"
]

# Write the data to the file
with open('item_settings.toml', 'w') as f:
    for part in data_parts:
        f.write(part)
