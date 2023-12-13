import tkinter as tk
from tkinter import ttk, messagebox
import json
import webbrowser
import subprocess

def create_settings_file():
    # Call the Python script
    subprocess.run(["python", "Generate_item_settings_file.py"])
    
# Initialize the list
item_list = []

def load_items():
    # Load the items from the file
    try:
        with open('items.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

def add_or_update_item():
    # Get the values from the entry fields
    modid = modid_entry.get()
    item = item_entry.get()
    hydration = hydration_scale.get()
    quenching = quenching_scale.get()

    # Combine the modid and item to form the item-id
    item_id = f"{modid}:{item}"

    # Load the existing items from the file
    try:
        with open(f'{item_type.get()}.json', 'r') as f:
            existing_items = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        existing_items = []

    # Check if the item already exists in the list
    for i, existing_item in enumerate(existing_items):
        if existing_item[0] == item_id:
            # Update the existing item
            existing_items[i] = [item_id, hydration, quenching]
            break
    else:
        # Add the new item to the list
        existing_items.append([item_id, hydration, quenching])

    # Save the list to the appropriate file based on the selected item type
    with open(f'{item_type.get()}.json', 'w') as f:
        json.dump(existing_items, f)

    # Update the treeview
    update_treeview()

def delete_item():
    # Get the selected item
    selected_item = treeview.selection()

    # Check if an item is selected
    if not selected_item:
        messagebox.showinfo("Error", "No item selected!")
        return

    # Delete the selected item from the list
    item_id = treeview.item(selected_item)['values'][0]
    item_list.remove([item_id, hydration_scale.get(), quenching_scale.get()])

    # Save the list to a file
    with open('items.json', 'w') as f:
        json.dump(item_list, f)

    # Update the treeview
    update_treeview()

def update_treeview(*args):
    # Load the items from the food and drink files
    try:
        with open('food.json', 'r') as f:
            food_items = json.load(f)
    except FileNotFoundError:
        food_items = []

    try:
        with open('drink.json', 'r') as f:
            drink_items = json.load(f)
    except FileNotFoundError:
        drink_items = []

    # Get the search term from the StringVar
    search_term = search_var.get()

    # Get the current selection
    selected_item = treeview.selection()

    # Clear the current items in the treeview
    treeview.delete(*treeview.get_children())

    # Create a separate list for the search results
    search_results = []

    # Add each item to the search results if it matches the search term
    for item in item_list:
        if search_term.lower() in item[0].lower():
            search_results.append(item)

    # Add each item in the search results to the treeview
    for item in search_results:
        # Determine the item type
        if item in food_items:
            item_type = 'Food'
        elif item in drink_items:
            item_type = 'Drink'
        else:
            item_type = 'Unknown'

        treeview.insert('', 'end', values=item + [item_type])

    # Restore the selection
    if selected_item:
        treeview.selection_set(selected_item)

def load_item(event):
    # Get the selected item
    selected_item = treeview.selection()

    # Check if an item is selected
    if not selected_item:
        return

    # Load the values into the entry fields
    item_id, hydration, quenching, item_type = treeview.item(selected_item[0])['values']
    modid, item = item_id.split(":")
    modid_entry.delete(0, tk.END)
    modid_entry.insert(0, modid)
    item_entry.delete(0, tk.END)
    item_entry.insert(0, item)
    hydration_scale.set(hydration)
    quenching_scale.set(quenching)

def set_item(modid, item):
    # Set the values of the entry fields
    modid_entry.delete(0, tk.END)
    modid_entry.insert(0, modid.lower())
    item_entry.delete(0, tk.END)
    item_entry.insert(0, item.lower().replace(' ', '_'))

# Load the existing items
item_list = load_items()

# Create the main window
root = tk.Tk()
root.title("Azureddraig's Thirst was Taken Helper")  # Set the title of the window
root.geometry("900x600")  # Set the window size
root.grid_columnconfigure(0, weight=1)  # Allows column to stretch upon resizing
root.configure(bg='#5DA6C3')  # Set the background color

# Create the labels and entry fields
tk.Label(root, text="Mod:", bg='#5DA6C3').grid(row=0, column=0, sticky=tk.W)
modid_entry = tk.Entry(root)
modid_entry.grid(row=1, column=0, sticky=tk.E+tk.W)  # This makes the entry widget expand horizontally

tk.Label(root, text="Item:", bg='#5DA6C3').grid(row=2, column=0, sticky=tk.W)
item_entry = tk.Entry(root)
item_entry.grid(row=3, column=0, sticky=tk.E+tk.W)

tk.Label(root, text="Thirst amount:", bg='#5DA6C3').grid(row=4, column=0, sticky=tk.W)
hydration_scale = tk.Scale(root, from_=-10, to=20, resolution=1, orient=tk.HORIZONTAL)
hydration_scale.grid(row=5, column=0, sticky=tk.E+tk.W)

tk.Label(root, text="Quench Amount:", bg='#5DA6C3').grid(row=6, column=0, sticky=tk.W)
quenching_scale = tk.Scale(root, from_=-10, to=20, resolution=1, orient=tk.HORIZONTAL)
quenching_scale.grid(row=7, column=0, sticky=tk.E+tk.W)

# Create the radio buttons for item type
item_type = tk.StringVar(value='food')
tk.Radiobutton(root, text='Food', variable=item_type, value='food').grid(row=8, column=0, sticky=tk.W)
tk.Radiobutton(root, text='Drink', variable=item_type, value='drink').grid(row=9, column=0, sticky=tk.W)

# Create the add button
add_button = tk.Button(root, text="Add or Update Item", command=add_or_update_item, bg='green')
add_button.grid(row=10, column=0, sticky=tk.E+tk.W)

# Create a frame
frame = tk.Frame(root)
frame.grid(row=15, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

# Configure the grid to expand
root.grid_rowconfigure(15, weight=1)  # Only the row containing the frame will expand
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create the treeview inside the frame with an additional "Item Type" column
treeview = ttk.Treeview(frame, columns=("Item ID", "Thirst Amount", "Quench Amount", "Item Type"), show='headings')
treeview.heading("Item ID", text="Item ID")
treeview.heading("Thirst Amount", text="Thirst Amount")
treeview.heading("Quench Amount", text="Quench Amount")
treeview.heading("Item Type", text="Item Type")  # New column header
treeview.pack(fill=tk.BOTH, expand=True)  # This makes the treeview expand horizontally and vertically within the frame

# Create a scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)

# Configure the treeview to use the scrollbar
treeview.configure(yscrollcommand=scrollbar.set)

# Pack the treeview and the scrollbar
treeview.pack(side="left", fill=tk.BOTH, expand=True)
scrollbar.pack(side="right", fill="y")

treeview.bind('<<TreeviewSelect>>', load_item)  # Bind the load_item function to the treeview's select event

# Create the delete button
delete_button = tk.Button(root, text="Delete Item", command=delete_item, bg='red')
delete_button.grid(row=13, column=0, sticky=tk.E+tk.W)

# Create the "Common Items from Mods" menubutton
mods_menubutton = tk.Menubutton(root, text="Common Items from Mods", relief=tk.RAISED)
mods_menubutton.grid(row=11, column=0, sticky=tk.E+tk.W)
 
# Create the "Common Items from Mods" menu
mods_menu = tk.Menu(mods_menubutton, tearoff=0)
mods_menubutton.configure(menu=mods_menu)
 
# Create the mod menus
croptopia_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Croptopia", menu=croptopia_menu)

# Create the "Crops" menu under "Croptopia"
crops_menu = tk.Menu(croptopia_menu, tearoff=0)
croptopia_menu.add_cascade(label="Crops", menu=crops_menu)
 
# Create the "Fruits" menu under "Crops"
fruits_menu = tk.Menu(crops_menu, tearoff=0)
crops_menu.add_cascade(label="Fruits", menu=fruits_menu)
 
# Add a command to open the web page
fruits_menu.add_command(label="https://croptopia.fandom.com/wiki/Crops#Fruits", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Crops#Fruits"))
 
# Add items to the "Fruits" menu
fruits = ["Blackberry", "Blueberry", "Cantaloupe", "Cranberry", "Currant", "Elderberry", "Grape", "Honeydew", "Kiwi", "Pineapple", "Raspberry", "Saguaro", "Strawberry"]
for fruit in fruits:
    fruits_menu.add_command(label=fruit, command=lambda fruit=fruit: set_item("Croptopia", fruit))
 
# Create the "Vegetables" menu under "Crops"
vegetables_menu = tk.Menu(crops_menu, tearoff=0)
crops_menu.add_cascade(label="Vegetables", menu=vegetables_menu)
 
# Add a command to open the web page
vegetables_menu.add_command(label="https://croptopia.fandom.com/wiki/Crops#Vegetables", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Crops#Vegetables"))
 
# Add items to the "Vegetables" menu
vegetables = ["Artichoke", "Asparagus", "Bell Pepper", "Black Bean", "Broccoli", "Cabbage", "Cauliflower", "Celery", "Chile Pepper", "Corn", "Cucumber", "Eggplant", "Garlic", "Green Bean", "Green Onion", "Hops", "Kale", "Leek", "Lettuce", "Olive", "Onion", "Radish", "Rhubarb", "Rutabaga", "Soybean", "Spinach", "Squash", "Sweet Potato", "Tomatillo", "Tomato", "Turnip", "Yam", "Zucchini"]
for vegetable in vegetables:
    vegetables_menu.add_command(label=vegetable, command=lambda vegetable=vegetable: set_item("Croptopia", vegetable))
 
# Create the "Other" menu under "Crops"
other_menu = tk.Menu(crops_menu, tearoff=0)
crops_menu.add_cascade(label="Other", menu=other_menu)
 
# Add a command to open the web page
other_menu.add_command(label="https://croptopia.fandom.com/wiki/Crops#Other", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Crops#Other"))
 
# Add items to the "Other" menu
other = ["Coffee Beans","Peanut","Rice","Mustard","Turmeric","Ginger","Basil","Oats","Barley","Vanilla","Pepper","Tea"]
for other_item in other:
    other_menu.add_command(label=other_item, command=lambda other_item=other_item: set_item("Croptopia", other_item))
 
# Create the "Tree Crops" menu under "Crops"
tree_crops_menu = tk.Menu(crops_menu, tearoff=0)
crops_menu.add_cascade(label="Tree Crops", menu=tree_crops_menu)
 
# Add a command to open the web page
tree_crops_menu.add_command(label="https://croptopia.fandom.com/wiki/Crops#Tree_Crops", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Crops#Tree_Crops"))
 
# Add items to the "Tree Crops" menu
tree_crops = ["Apple","Banana","Orange","Persimmon","Plum","Cherry","Lemon","Grapefruit","Kumquat","Peach","Coconut","Nutmeg","Fig","Nectarine","Mango","Dragon Fruit","Star Fruit","Avocado","Apricot","Pear","Lime","Date","Almond","Cashew","Pecan","Walnut","Cinnamon"]
for tree_crop in tree_crops:
    tree_crops_menu.add_command(label=tree_crop, command=lambda tree_crop=tree_crop: set_item("Croptopia", tree_crop))

# Create the "Drinks" menu under "Croptopia"
drinks_menu = tk.Menu(croptopia_menu, tearoff=0)
croptopia_menu.add_cascade(label="Drinks", menu=drinks_menu)

# Add a command to open the web page
drinks_menu.add_command(label="https://croptopia.fandom.com/wiki/Drinks", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Drinks"))

# Create the "Juice" menu under "Drinks"
juice_menu = tk.Menu(drinks_menu, tearoff=0)
drinks_menu.add_cascade(label="Juice", menu=juice_menu)

# Add items to the "Juice" menu
juices = ["Apple Juice","Cranberry Juice","Grape Juice","Melon Juice","Orange Juice","Pineapple Juice","Saguaro Juice","Tomato Juice"]
for juice in juices:
    juice_menu.add_command(label=juice, command=lambda juice=juice: set_item("croptopia", juice))

# Create the "Smoothies" menu under "Drinks"
smoothies_menu = tk.Menu(drinks_menu, tearoff=0)
drinks_menu.add_cascade(label="Smoothies", menu=smoothies_menu)

# Add items to the "Smoothies" menu
smoothies = ["Banana Smoothie","Kale Smoothie","Fruit Smoothie","Strawberry Smoothie"]
for smoothie in smoothies:
    smoothies_menu.add_command(label=smoothie, command=lambda smoothie=smoothie: set_item("croptopia", smoothie))

# Create the "Other" menu under "Drinks"
other_drinks_menu = tk.Menu(drinks_menu, tearoff=0)
drinks_menu.add_cascade(label="Other", menu=other_drinks_menu)

# Add items to the "Other" menu
other_drinks = ["Cherry Soda","Chocolate Milkshake","Coffee","Grape Soda","Limeade","Lemonade","Lemon-Lime Soda","Orange Soda","Pumpkin Spice Latte","Rum","Tea","Wine"]
for other_drink in other_drinks:
    other_drinks_menu.add_command(label=other_drink, command=lambda other_drink=other_drink: set_item("croptopia", other_drink))

# Create the "Foods" menu under "Croptopia"
foods_menu = tk.Menu(croptopia_menu, tearoff=0)
croptopia_menu.add_cascade(label="Foods", menu=foods_menu)

# Add a command to open the web pages
foods_menu.add_command(label="https://croptopia.fandom.com/wiki/Food", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Food"))
foods_menu.add_command(label="https://croptopia.fandom.com/wiki/Seafood", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Seafood"))

# Add items to the "Foods" menu
foods = ["Sticky Toffee Pudding", "Trifle", "Ajvar", "Ajvar Toast", "Avocado Toast", "Beef Stew", "Beef Stir Fry", "Buttered Green Beans", "Cheesy Asparagus", "Chocolate Ice Cream", "Eggplant Parmesan", "Fruit Cake", "Grilled Eggplant", "Kiwi Sorbet", "Lemon Coconut Bar", "Nether Wart Stew", "Peanut Butter", "Peanut Butter W Celery", "Raw Bacon", "Rhubarb Crisp", "Roasted Asparagus", "Roasted Radishes", "Roasted Squash", "Roasted Turnips", "Steamed Broccoli", "Steamed Green Beans", "Stir Fry", "Stuffed Artichoke", "Toast Sandwich", "Roasted Pumpkin Seeds", "Roasted Sunflower Seeds", "Pumpkin Bars", "Corn Bread", "Pumpkin Soup", "Meringue", "Cabbage Roll", "Borscht", "Goulash", "Beetroot Salad", "Candied Kumquats", "Steamed Crab", "Sea Lettuce", "Deep Fried Shrimp", "Tuna Roll", "Fried Calamari", "Crab Legs", "Steamed Clams", "Grilled Oysters", "Anchovy Pizza", "Mashed Potatoes", "Baked Crepes", "Cinnamon Roll", "Croque Madame", "Croque Monsieur", "Dauphine Potatoes", "Fried Frog Legs", "Frog Legs", "Ground Pork", "Hashed Brown", "Macaron", "Quiche", "Sausage", "Sunny Side Eggs", "Sweet Crepes", "The Big Breakfast", "Anchovy", "Calamari", "Clam", "Crab", "Glowing Calamari", "Oyster", "Roe", "Shrimp", "Tuna", "Baked Beans", "Baked Sweet Potato", "Baked Yam", "Caramel", "Cooked Anchovy", "Cooked Bacon", "Cooked Calamari", "Cooked Shrimp", "Cooked Tuna", "Popcorn", "Raisins", "Toast", "Apricot Jam", "Blackberry Jam", "Blueberry Jam", "Cherry Jam", "Elderberry Jam", "Grape Jam", "Peach Jam", "Raspberry Jam", "Strawberry Jam", "Mango Ice Cream", "Pecan Ice Cream", "Strawberry Ice Cream", "Vanilla Ice Cream", "Apple Pie", "Cherry Pie", "Pecan Pie", "Rhubarb Pie", "Beef Jerky", "Pork Jerky", "Kale Chips", "Potato Chips", "Steamed Rice", "French Fries", "Sweet Potato Fries", "Onion Rings", "Doughnut", "Cucumber Salad", "Caesar Salad", "Leafy Salad", "Fruit Salad", "Veggie Salad", "Pork And Beans", "Oatmeal", "Yoghurt", "Saucy Chips", "Roasted Nuts", "Trail Mix", "Protein Bar", "Nougat", "Scrambled Eggs", "Buttered Toast", "Toast With Jam", "Ham Sandwich", "Peanut Butter And Jam", "Blt", "Grilled Cheese", "Tuna Sandwich", "Cheeseburger", "Hamburger", "Tofuburger", "Pizza", "Supreme Pizza", "Cheese Pizza", "Pineapple Pepperoni Pizza", "Lemon Chicken", "Fried Chicken", "Chicken And Noodles", "Chicken And Dumplings", "Tofu And Dumplings", "Spaghetti Squash", "Chicken And Rice", "Taco", "Sushi", "Egg Roll", "Cashew Chicken", "Yam Jam", "Banana Cream Pie", "Candy Corn", "Rum Raisin Ice Cream", "Cheese Cake", "Brownies", "Snicker Doodle", "Banana Nut Bread", "Candied Nuts", "Almond Brittle", "Oatmeal Cookie", "Nutty Cookie", "Burrito", "Tostada", "Carnitas", "Fajitas", "Enchilada", "Churros", "Tamales", "Tres Leche Cake", "Stuffed Poblanos", "Chili Relleno", "Crema", "Refried Beans", "Chimichanga", "Quesadilla", "Corn Husk", "Whipping Cream", "Shepherds Pie", "Beef Wellington", "Fish And Chips", "Eton Mess", "Cornish Pasty", "Scones", "Figgy Pudding", "Treacle Tart"]
foods.sort()
for food in foods:
    foods_menu.add_command(label=food, command=lambda food=food: set_item("croptopia", food))

# Create the "Ingredients" menu under "Croptopia"
ingredients_menu = tk.Menu(croptopia_menu, tearoff=0)
croptopia_menu.add_cascade(label="Ingredients", menu=ingredients_menu)

# Add a command to open the web page
ingredients_menu.add_command(label="https://croptopia.fandom.com/wiki/Ingredients", command=lambda: webbrowser.open("https://croptopia.fandom.com/wiki/Ingredients"))

# Add items to the "Ingredients" menu
ingredients = ["Butter", "Caramel", "Cheese", "Cinnamon", "Corn Husk", "Crema", "Dough", "Flour", "Milk Bottle", "Molasses", "Noodle", "Olive Oil", "Pepper", "Pepperoni", "Ravioli", "Salt", "Soy Milk", "Soy Sauce", "Tea Leaves", "Water Bottle", "Whipping Cream"]
ingredients.sort()
for ingredient in ingredients:
    ingredients_menu.add_command(label=ingredient, command=lambda ingredient=ingredient: set_item("croptopia", ingredient))

# Create the "Pam's Harvestcraft 2" menu
harvestcraft_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Pam's Harvestcraft 2", menu=harvestcraft_menu)

# Create the submenus under "Pam's Harvestcraft 2"
# Create the "Harvestcraft 2 Crops" menu under "Pam's Harvestcraft 2"
harvestcraft_crops_menu = tk.Menu(harvestcraft_menu, tearoff=0)
harvestcraft_menu.add_cascade(label="Harvestcraft 2 Crops", menu=harvestcraft_crops_menu)

# Add items to the "Harvestcraft 2 Crops" menu
crops = ["Bell Pepper", "Blackberry", "Blueberry", "Cactus Fruit", "Candleberry", "Cantaloupe", "Cranberry", "Cucumber", "Elderberry", "Grape", "Green Grape", "Huckleberry", "Juniper Berry", "Kiwi", "Mulberry", "Raspberry", "Strawberry", "Tomatillo", "Tomato", "Barrel Cactus", "Nopales", "Wolfberry", "Pineapple", "Cloudberry", "Guarana", "Cabbage", "Lettuce", "Corn"]
crops.sort()
for crop in crops:
    harvestcraft_crops_menu.add_command(label=crop, command=lambda crop=crop: set_item("pamhc2crops", crop.replace(' ', '').lower() + "item"))

# Create the "Harvestcraft 2 Food Core" menu under "Pam's Harvestcraft 2"
harvestcraft_food_core_menu = tk.Menu(harvestcraft_menu, tearoff=0)
harvestcraft_menu.add_cascade(label="Harvestcraft 2 Food Core", menu=harvestcraft_food_core_menu)

# Create the "Drinks" and "Food" submenus under "Harvestcraft 2 Food Core"
harvestcraft_drinks_menu = tk.Menu(harvestcraft_food_core_menu, tearoff=0)
harvestcraft_food_core_menu.add_cascade(label="Drinks", menu=harvestcraft_drinks_menu)

harvestcraft_food_menu = tk.Menu(harvestcraft_food_core_menu, tearoff=0)
harvestcraft_food_core_menu.add_cascade(label="Food", menu=harvestcraft_food_menu)

# Add items to the "Drinks" submenu
drinks = ["Cream", "Hot Chocolate", "Apple Juice", "Apple Smoothie", "Melon Juice", "Melon Smoothie", "Sweet Berry Juice", "Sweet Berry Smoothie", "Glow Berry Juice", "Glow Berry Smoothie", "Fresh Milk", "Fresh Water", "Fruit Punch", "P8 Juice"]
drinks.sort()
for drink in drinks:
    harvestcraft_drinks_menu.add_command(label=drink, command=lambda drink=drink: set_item("pamhc2foodcore", drink.replace(' ', '').lower() + "item"))

# Add items to the "Food" submenu
foods = ["Apple Sauce", "Cookies and Milk", "Potato Soup", "Carrot Soup", "Pumpkin Soup", "Stock", "Stew"]
foods.sort()
for food in foods:
    harvestcraft_food_menu.add_command(label=food, command=lambda food=food: set_item("pamhc2foodcore", food.replace(' ', '').lower() + "item"))

# Create the "Harvestcraft 2 Food Extended" menu under "Pam's Harvestcraft 2"
harvestcraft_food_extended_menu = tk.Menu(harvestcraft_menu, tearoff=0)
harvestcraft_menu.add_cascade(label="Harvestcraft 2 Food Extended", menu=harvestcraft_food_extended_menu)

# Create the "Food" and "Drinks" submenus under "Harvestcraft 2 Food Extended"
harvestcraft_food_menu = tk.Menu(harvestcraft_food_extended_menu, tearoff=0)
harvestcraft_food_extended_menu.add_cascade(label="Food", menu=harvestcraft_food_menu)

harvestcraft_drinks_menu = tk.Menu(harvestcraft_food_extended_menu, tearoff=0)
harvestcraft_food_extended_menu.add_cascade(label="Drinks", menu=harvestcraft_drinks_menu)

# Add items to the "Food" submenu
foods = ["Fiesta Corn Salad", "Chicken Noodle Soup", "Cornflakes", "Cranberry Sauce", "Crispy Rice Puff Cereal", "Berry Vinaigrette Salad", "Caesar Salad", "Chicken Curry", "Chicken Gumbo", "Choco Voxels", "Citrus Salad", "Creamed Broccoli Soup", "Cream of Avocado Soup", "Cucumber Sandwich", "Curry", "Dhal", "Garden Soup", "Guiso", "Hot and Sour Soup", "Lamb Barley Soup", "Leek Bacon Soup", "Mixed Flower Salad", "Mixed Salad", "Nopales Salad", "Old World Veggie Soup", "Pea and Ham Soup", "Pho", "Pizza Soup", "Potato Leek Soup", "Ramen", "Seed Soup", "Spicy Greens", "Split Pea Soup", "Spring Salad", "Sunflower Broccoli Salad", "Succotash", "Three Bean Salad", "Tomato Soup", "Vegetable Soup", "Wonton Soup", "Cream of Chicken", "Cream of Mushroom", "Wonton Soup"]
foods.sort()
for food in foods:
    harvestcraft_food_menu.add_command(label=food, command=lambda food=food: set_item("pamhc2foodextended", food.replace(' ', '').lower() + "item"))

# Add items to the "Drinks" submenu
drinks = ["Soy Milk", "Cherry Soda", "Cola Soda", "Energy Drink", "Ginger Soda", "Grapefruit Soda", "Grape Soda", "Lemon Lime Soda", "Orange Soda", "Root Beer Float", "Root Beer Soda", "Strawberry Soda", "Carrot Juice", "Chocolate Milk", "Apple Cider", "Chai Tea", "Chocolate Milkshake", "Coffee Con Leche", "Dandelion Tea", "Earl Grey Tea", "Eggnog", "Espresso", "Green Tea", "Lemon Aid", "Pina Colada", "Pumpkin Spice Latte", "Rose Petal Tea", "Sunday High Tea", "Sweet Tea", "Hazelnut Coffee", "Blackberry Juice", "Blueberry Juice", "Cactus Fruit Juice", "Candleberry Juice", "Cranberry Juice", "Elderberry Juice", "Huckleberry Juice", "Juniper Berry Juice", "Mulberry Juice", "Raspberry Juice", "Strawberry Juice", "Cantaloupe Juice", "Grape Juice", "Green Grape Juice", "Kiwi Juice", "Pineapple Juice", "Cherry Juice", "Orange Juice", "Peach Juice", "Pear Juice", "Plum Juice", "Pawpaw Juice", "Soursop Juice", "Apricot Juice", "Banana Juice", "Date Juice", "Dragonfruit Juice", "Fig Juice", "Grapefruit Juice", "Mango Juice", "Papaya Juice", "Persimmon Juice", "Pomegranate Juice", "Starfruit Juice", "Breadfruit Juice", "Jackfruit Juice", "Guava Juice", "Lychee Juice", "Passionfruit Juice", "Rambutan Juice", "Tamarind Juice", "Gooseberry Juice", "Durian Juice", "Lemon Juice", "Lime Juice", "Blackberry Smoothie", "Blueberry Smoothie", "Cactus Fruit Smoothie", "Candleberry Smoothie", "Cranberry Smoothie", "Elderberry Smoothie", "Huckleberry Smoothie", "Juniper Berry Smoothie", "Mulberry Smoothie", "Raspberry Smoothie", "Strawberry Smoothie", "Cantaloupe Smoothie", "Grape Smoothie", "Green Grape Smoothie", "Kiwi Smoothie", "Pineapple Smoothie", "Cherry Smoothie", "Orange Smoothie", "Peach Smoothie", "Pear Smoothie", "Plum Smoothie", "Pawpaw Smoothie", "Soursop Smoothie", "Apricot Smoothie", "Banana Smoothie", "Date Smoothie", "Dragonfruit Smoothie", "Fig Smoothie", "Grapefruit Smoothie", "Mango Smoothie", "Papaya Smoothie", "Persimmon Smoothie", "Pomegranate Smoothie", "Starfruit Smoothie", "Breadfruit Smoothie", "Jackfruit Smoothie", "Guava Smoothie", "Lychee Smoothie", "Passionfruit Smoothie", "Rambutan Smoothie", "Tamarind Smoothie", "Gooseberry Smoothie", "Durian Smoothie", "Lemon Smoothie", "Lime Smoothie"]
drinks.sort()
for drink in drinks:
    harvestcraft_drinks_menu.add_command(label=drink, command=lambda drink=drink: set_item("pamhc2foodextended", drink.replace(' ', '').lower() + "item"))

# Create the "Harvestcraft 2 Trees" menu under "Pam's Harvestcraft 2"
harvestcraft_trees_menu = tk.Menu(harvestcraft_menu, tearoff=0)
harvestcraft_menu.add_cascade(label="Harvestcraft 2 Trees", menu=harvestcraft_trees_menu)

# Add items to the "Harvestcraft 2 Trees" menu
trees = ["Cherry", "Gooseberry", "Lemon", "Orange", "Peach", "Pear", "Plum", "Pawpaw", "Soursop", "Apricot", "Coconut", "Date", "Dragonfruit", "Durian", "Fig", "Grapefruit", "Lime", "Mango", "Papaya", "Persimmon", "Pomegranate", "Starfruit", "Guava", "Lychee", "Passionfruit", "Rambutan"]
trees.sort()
for tree in trees:
    harvestcraft_trees_menu.add_command(label=tree, command=lambda tree=tree: set_item("pamhc2trees", tree.replace(' ', '').lower() + "item"))

# Create the other mod menus
# Create the "Aether" menu
aether_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Aether", menu=aether_menu)

# Add items to the "Aether" menu
aether_items = ["Blue Berry", "Enchanted Berry", "White Apple", "Skyroot Milk Bucket"]
for item in aether_items:
    aether_menu.add_command(label=item, command=lambda item=item: set_item("aether", item.replace(' ', '_').lower()))

# Create the "Farmer's Delight" menu
farmers_delight_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Farmer's Delight", menu=farmers_delight_menu)

# Create the "Drinks" and "Foods" submenus under "Farmer's Delight"
farmers_delight_drinks_menu = tk.Menu(farmers_delight_menu, tearoff=0)
farmers_delight_menu.add_cascade(label="Drinks", menu=farmers_delight_drinks_menu)

farmers_delight_foods_menu = tk.Menu(farmers_delight_menu, tearoff=0)
farmers_delight_menu.add_cascade(label="Foods", menu=farmers_delight_foods_menu)

# Add items to the "Drinks" submenu
drinks = ["Apple Cider", "Melon Juice", "Milk Bottle", "Hot Cocoa"]
for drink in drinks:
    farmers_delight_drinks_menu.add_command(label=drink, command=lambda drink=drink: set_item("farmersdelight", drink.replace(' ', '_').lower()))

# Add items to the "Foods" submenu
foods = ["Pumpkin Slice", "Cabbage Leaf", "Melon Popsicle", "Fruit Salad", "Tomato Sauce", "Mixed Salad", "Beef Stew", "Chicken Soup", "Vegetable Soup", "Fish Stew", "Pumpkin Soup", "Baked Cod Stew", "Noodle Soup", "Cabbage", "Tomato", "Nether Salad", "Bone Broth"]
for food in foods:
    farmers_delight_foods_menu.add_command(label=food, command=lambda food=food: set_item("farmersdelight", food.replace(' ', '_').lower()))

# Create the "Addons" menu under "Farmer's Delight"
addons_menu = tk.Menu(farmers_delight_menu, tearoff=0)
farmers_delight_menu.add_cascade(label="Addons", menu=addons_menu)

# Create the "Crabber's Delight" menu under "Addons"
crabbers_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="Crabber's Delight", menu=crabbers_delight_menu)

# Add items to the "Crabber's Delight" menu
crabbers_delight_items = ["Clam Chowder", "Bisque", "Seafood Gumbo", "Kelp Shake"]
for item in crabbers_delight_items:
    crabbers_delight_menu.add_command(label=item, command=lambda item=item: set_item("crabbersdelight", item.replace(' ', '_').lower()))

# Create the "Twilight Delight" menu under "Addons"
twilight_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="Twilight Delight", menu=twilight_delight_menu)

# Add items to the "Twilight Delight" menu
twilight_delight_items = ["Glow Stew", "Mushgloom Sauce", "Thousand Plant Stew", "Borer Tear Soup"]
for item in twilight_delight_items:
    twilight_delight_menu.add_command(label=item, command=lambda item=item: set_item("twilightdelight", item.replace(' ', '_').lower()))
    
# Create the "Ocean's Delight" menu under "Addons"
oceans_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="Ocean's Delight", menu=oceans_delight_menu)

# Add items to the "Ocean's Delight" menu
oceans_delight_items = ["Guardian Soup", "Bowl of Guardian Soup", "Seagrass Salad"]
for item in oceans_delight_items:
    oceans_delight_menu.add_command(label=item, command=lambda item=item: set_item("oceansdelight", item.replace(' ', '_').lower()))

# Create the "End's Delight" menu under "Addons"
ends_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="End's Delight", menu=ends_delight_menu)

# Create the "Drinks" and "Food" submenus under "End's Delight"
ends_delight_drinks_menu = tk.Menu(ends_delight_menu, tearoff=0)
ends_delight_menu.add_cascade(label="Drinks", menu=ends_delight_drinks_menu)

ends_delight_food_menu = tk.Menu(ends_delight_menu, tearoff=0)
ends_delight_menu.add_cascade(label="Food", menu=ends_delight_food_menu)

# Add items to the "Drinks" submenu
ends_delight_drinks = ["Chorus Fruit Wine", "Chorus Fruit Milk Tea", "Bubble Tea", "Dragons Breath Soda", "Chorus Flower Tea"]
for drink in ends_delight_drinks:
    ends_delight_drinks_menu.add_command(label=drink, command=lambda drink=drink: set_item("ends_delight", drink.replace(' ', '_').lower()))

# Add items to the "Food" submenu
ends_delight_food = ["Ender Sauce", "Chorus Fruit Popsicle", "End Mixed Salad", "Assorted Salad"]
for food in ends_delight_food:
    ends_delight_food_menu.add_command(label=food, command=lambda food=food: set_item("ends_delight", food.replace(' ', '_').lower()))

# Create the "Ender's Delight" menu under "Addons"
enders_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="Ender's Delight", menu=enders_delight_menu)

# Add items to the "Ender's Delight" menu
enders_delight_items = ["Chorus Stew", "Chorus Stew (Wood)", "Twisted Cereal", "Twisted Cereal (Wood)", "Endermite Stew", "Endermite Stew (Wood)"]
for item in enders_delight_items:
    enders_delight_menu.add_command(label=item, command=lambda item=item: set_item("endersdelight", item.replace(' ', '_').lower()))

# Create the "Corn Delight" menu under "Addons"
corn_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="Corn Delight", menu=corn_delight_menu)

# Add items to the "Corn Delight" menu
corn_delight_items = ["Creamy Corn Drink", "Corn Soup"]
for item in corn_delight_items:
    corn_delight_menu.add_command(label=item, command=lambda item=item: set_item("corn_delight", item.replace(' ', '_').lower()))

# Create the "Pineapple Delight" menu under "Addons"
pineapple_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="Pineapple Delight", menu=pineapple_delight_menu)

# Add items to the "Pineapple Delight" menu
pineapple_delight_items = ["Pineapple Juice", "Pineapple Milkshake", "Pineapple", "Pineapple Side"]
for item in pineapple_delight_items:
    pineapple_delight_menu.add_command(label=item, command=lambda item=item: set_item("pineapple_delight", item.replace(' ', '_').lower()))

# Create the "Quality's Delight" menu under "Addons"
qualitys_delight_menu = tk.Menu(addons_menu, tearoff=0)
addons_menu.add_cascade(label="Quality's Delight", menu=qualitys_delight_menu)

# Add items to the "Quality's Delight" menu
qualitys_delight_items = ["Seafood Gumbo (Iron Quality)", "Seafood Gumbo (Gold Quality)", "Seafood Gumbo (Diamond Quality)", "Bisque (Iron Quality)", "Bisque (Gold Quality)", "Bisque (Diamond Quality)", "Clam Chowder (Iron Quality)", "Clam Chowder (Gold Quality)", "Clam Chowder (Diamond Quality)", "Cabbage (Iron Quality)", "Cabbage (Gold Quality)", "Cabbage (Diamond Quality)", "Cabbage Leaf (Iron Quality)", "Cabbage Leaf (Gold Quality)", "Cabbage Leaf (Diamond Quality)", "Tomato (Iron Quality)", "Tomato (Gold Quality)", "Tomato (Diamond Quality)", "Melon Popsicle (Iron Quality)", "Melon Popsicle (Gold Quality)", "Melon Popsicle (Diamond Quality)", "Tomato Sauce (Iron Quality)", "Tomato Sauce (Gold Quality)", "Tomato Sauce (Diamond Quality)", "Mixed Salad (Iron Quality)", "Mixed Salad (Gold Quality)", "Mixed Salad (Diamond Quality)", "Fruit Salad (Iron Quality)", "Fruit Salad (Gold Quality)", "Fruit Salad (Diamond Quality)", "Bone Broth (Iron Quality)", "Bone Broth (Gold Quality)", "Bone Broth (Diamond Quality)", "Beef Stew (Iron Quality)", "Beef Stew (Gold Quality)", "Beef Stew (Diamond Quality)", "Chicken Soup (Iron Quality)", "Chicken Soup (Gold Quality)", "Chicken Soup (Diamond Quality)", "Vegetable Soup (Iron Quality)", "Vegetable Soup (Gold Quality)", "Vegetable Soup (Diamond Quality)", "Fish Stew (Iron Quality)", "Fish Stew (Gold Quality)", "Fish Stew (Diamond Quality)", "Baked Cod Stew (Iron Quality)", "Baked Cod Stew (Gold Quality)", "Baked Cod Stew (Diamond Quality)", "Noodle Soup (Iron Quality)", "Noodle Soup (Gold Quality)", "Noodle Soup (Diamond Quality)", "Bowl of Guardian Soup (Iron Quality)", "Bowl of Guardian Soup (Gold Quality)", "Bowl of Guardian Soup (Diamond Quality)", "Guardian Soup (Iron Quality)", "Guardian Soup (Gold Quality)", "Guardian Soup (Diamond Quality)"]
for item in qualitys_delight_items:
    item_name, quality = item.split(" (")
    quality = quality.replace(" Quality)", "").lower()
    qualitys_delight_menu.add_command(label=item, command=lambda item=item, quality=quality: set_item("qualitysdelight", f"{item_name.replace(' ', '_').lower()}_{quality}"))

# Create the "Caupona" menu
caupona_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Caupona", menu=caupona_menu)

# Create the "Drinks" and "Food" submenus under "Caupona"
caupona_drinks_menu = tk.Menu(caupona_menu, tearoff=0)
caupona_menu.add_cascade(label="Drinks", menu=caupona_drinks_menu)

caupona_food_menu = tk.Menu(caupona_menu, tearoff=0)
caupona_menu.add_cascade(label="Food", menu=caupona_food_menu)

# Add items to the "Drinks" submenu
drinks = ["Water", "Milk", "Scalded Milk"]
for drink in drinks:
    caupona_drinks_menu.add_command(label=drink, command=lambda drink=drink: set_item("caupona", drink))

# Add items to the "Food" submenu
foods = ["Acquacotta", "Bisque", "Borscht", "Borscht (Cream)", "Congee", "Cream of Meat Soup", "Cream of Mushroom Soup", "Dilute Soup", "Egg Drop Soup", "Egg Tongsui", "Fish Chowder", "Fish Soup", "Goji Tongsui", "Gruel", "Meat Soup", "Mushroom Soup", "Nail Soup", "Nettle Soup", "Okroshka", "Poultry Soup", "Pumpkin Soup", "Pumpkin Soup (Cream)", "Seaweed Soup", "Stock", "Stracciatella", "Ukha", "Vegetable Chowder", "Vegetable Soup", "Walnut Soup"]
for food in foods:
    caupona_food_menu.add_command(label=food, command=lambda food=food: set_item("caupona", food))

# Create the "Quality Crops" menu
quality_crops_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Quality Crops", menu=quality_crops_menu)

# Add items to the "Quality Crops" menu
quality_crops = ["Carrot (Iron Quality)", "Carrot (Gold Quality)", "Carrot (Diamond Quality)", "Beetroot (Iron Quality)", "Beetroot (Gold Quality)", "Beetroot (Diamond Quality)", "Sweet Berries (Iron Quality)", "Sweet Berries (Gold Quality)", "Sweet Berries (Diamond Quality)", "Glow Berries (Iron Quality)", "Glow Berries (Gold Quality)", "Glow Berries (Diamond Quality)", "Beetroot Soup (Iron Quality)", "Beetroot Soup (Gold Quality)", "Beetroot Soup (Diamond Quality)", "Mushroom Stew (Iron Quality)", "Mushroom Stew (Gold Quality)", "Mushroom Stew (Diamond Quality)", "Rabbit Stew (Iron Quality)", "Rabbit Stew (Gold Quality)", "Rabbit Stew (Diamond Quality)", "Apple (Iron Quality)", "Apple (Gold Quality)", "Apple (Diamond Quality)", "Melon Slice (Iron Quality)", "Melon Slice (Gold Quality)", "Melon Slice (Diamond Quality)"]
quality_crops.sort()
for quality_crop in quality_crops:
    item, quality = quality_crop.split(" (")
    quality = quality.replace(" Quality)", "").lower()
    quality_crops_menu.add_command(label=quality_crop, command=lambda item=item, quality=quality: set_item("quality_crops", f"{item}_{quality}"))

# Create the "Drink Beer" menu
drink_beer_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Drink Beer", menu=drink_beer_menu)

# Add items to the "Drink Beer" menu
drink_beer_items = ["Beer Mug", "Beer Mug Blaze Stout", "Beer Mug Blaze Milk Stout", "Beer Mug Apple Lambic", "Beer Mug Sweet Berry Kriek", "Beer Mug Haars Icey Pale Lager", "Beer Mug Pumpkin Kvass", "Beer Mug Night Howl Kvass", "Beer Mug Frothy Pink Eggnog"]
for item in drink_beer_items:
    drink_beer_menu.add_command(label=item, command=lambda item=item: set_item("drinkbeer", item.replace(' ', '_').lower()))

# Create the "Raven Coffee" menu
raven_coffee_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Raven Coffee", menu=raven_coffee_menu)

# Add items to the "Raven Coffee" menu
raven_coffee_items = ["Large Brew Basic", "Large Brew Sugar", "Large Brew Apple", "Large Brew Berry", "Large Brew Honey", "Large Brew Chocolate", "Large Brew Milk", "Large Brew Mocha", "Large Brew Awkward", "Large Brew Carrot", "Large Brew Golden Carrot", "Large Brew Cookies and Cream", "Large Brew End", "Large Brew Melon", "Large Brew Golden Melon", "Large Brew Nether", "Large Brew Phantasm", "Large Brew Pumpkin Spice Latte", "Large Brew Pumpkin Spice Latte with Pumpkin", "Medium Brew Basic", "Medium Brew Sugar", "Medium Brew Apple", "Medium Brew Berry", "Medium Brew Honey", "Medium Brew Chocolate", "Medium Brew Milk", "Medium Brew Mocha", "Medium Brew Awkward", "Medium Brew Carrot", "Medium Brew Golden Carrot", "Medium Brew Cookies and Cream", "Medium Brew End", "Medium Brew Melon", "Medium Brew Golden Melon", "Medium Brew Nether", "Medium Brew Phantasm", "Medium Brew Pumpkin Spice Latte", "Medium Brew Pumpkin Spice Latte with Pumpkin", "Mug Brew Basic", "Mug Brew Sugar", "Mug Brew Apple", "Mug Brew Berry", "Mug Brew Honey", "Mug Brew Chocolate", "Mug Brew Milk", "Mug Brew Mocha", "Mug Brew Awkward", "Mug Brew Carrot", "Mug Brew Golden Carrot", "Mug Brew Cookies and Cream", "Mug Brew End", "Mug Brew Melon", "Mug Brew Golden Melon", "Mug Brew Nether", "Mug Brew Phantasm", "Mug Brew Pumpkin Spice Latte", "Mug Brew Pumpkin Spice Latte with Pumpkin", "Small Brew Basic"]
for item in raven_coffee_items:
    raven_coffee_menu.add_command(label=item, command=lambda item=item: set_item("ravencoffee", item.replace(' ', '_').lower()))

# Create the "Collector’s Reap" menu
collectors_reap_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Collector’s Reap", menu=collectors_reap_menu)

# Add items to the "Collector’s Reap" menu
collectors_reap_items = ["Lime Slice", "Lime", "Portobello Rice Soup", "Lime Popsicle"]
for item in collectors_reap_items:
    collectors_reap_menu.add_command(label=item, command=lambda item=item: set_item("collectorsreap", item.replace(' ', '_').lower()))

# Create the "Undergarden" menu
undergarden_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Undergarden", menu=undergarden_menu)

# Add items to the "Undergarden" menu
undergarden_items = ["Droopvine Item", "Blisterberry", "Rotten Blisterberry", "Bloody Stew", "Inky Stew", "Indigo Stew", "Veiled Stew"]
for item in undergarden_items:
    undergarden_menu.add_command(label=item, command=lambda item=item: set_item("undergarden", item.replace(' ', '_').lower()))

# Create the "Create" menu
create_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Create", menu=create_menu)

# Add items to the "Create" menu
create_items = ["Builder’s Tea"]
for item in create_items:
    create_menu.add_command(label=item, command=lambda item=item: set_item("create", item.replace(' ', '_').lower()))

# Create the "Brewin' and Chewin'" menu
brewinandchewin_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Brewin' and Chewin'", menu=brewinandchewin_menu)

# Add items to the "Brewin' and Chewin'" menu
brewinandchewin_items = ["Beer", "Vodka", "Rice Wine", "Mead", "Egg Grog", "Glittering Grenadine", "Bloody Mary", "Salty Folly", "Pale Jane", "Saccharine Rum", "Strongroot Ale", "Dread Nog", "Kombucha", "Red Rum", "Steel Toe Stout"]
for item in brewinandchewin_items:
    brewinandchewin_menu.add_command(label=item, command=lambda item=item: set_item("brewinandchewin", item.replace(' ', '_').lower()))

# Create the "Farmer's Respite'" menu
farmersrespite_menu = tk.Menu(mods_menu, tearoff=0)
mods_menu.add_cascade(label="Farmer's Respite'", menu=farmersrespite_menu)

# Add items to the "Farmer's Respite'" menu
farmersrespite_items = ["Green Tea", "Yellow Tea", "Black Tea", "Rose Hip Tea", "Dandelion Tea", "Coffee"]
for item in farmersrespite_items:
    farmersrespite_menu.add_command(label=item, command=lambda item=item: set_item("farmersrespite", item.replace(' ', '_').lower()))
    
# Add the rest of your code here for the other mod menus...

# Create the search label and entry field
tk.Label(root, text="Search:", bg='#5DA6C3').grid(row=18, sticky=tk.W)
search_var = tk.StringVar()
search_var.trace('w', update_treeview)
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.grid(row=19, sticky=tk.E+tk.W)

# Create the settings
create_button = tk.Button(root, text="Create Settings file", command=create_settings_file, bg='#99ccff')
create_button.grid(row=17, column=0, columnspan=2, rowspan = 2, sticky=tk.E+tk.W)

# Update the treeview with the existing items
update_treeview()
 
# Start the main loop
root.mainloop()
