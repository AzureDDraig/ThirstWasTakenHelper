import tkinter as tk
from tkinter import ttk, messagebox
import json
import webbrowser
 
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
 
    # Check if the item already exists in the list
    for i, existing_item in enumerate(item_list):
        if existing_item[0] == item_id:
            # Update the existing item
            item_list[i] = [item_id, hydration, quenching]
            break
    else:
        # Add the new item to the list
        item_list.append([item_id, hydration, quenching])
 
    # Save the list to a file
    with open('items.json', 'w') as f:
        json.dump(item_list, f)
 
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
 
def update_treeview():
    # Clear the current items in the treeview
    treeview.delete(*treeview.get_children())
 
    # Add each item to the treeview
    for item in item_list:
        treeview.insert('', 'end', values=item)
 
def load_item(event):
    # Get the selected item
    selected_item = treeview.selection()
 
    # Check if an item is selected
    if not selected_item:
        return
 
    # Load the values into the entry fields
    item_id, hydration, quenching = treeview.item(selected_item[0])['values']
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
root.geometry("800x600")  # Set the window size
root.grid_columnconfigure(0, weight=1)  # Allows column to stretch upon resizing
root.configure(bg='#5DA6C3')  # Set the background color
 
# Create the labels and entry fields
tk.Label(root, text="Mod:", bg='#5DA6C3').grid(row=0, sticky=tk.W)
modid_entry = tk.Entry(root)
modid_entry.grid(row=1, sticky=tk.E+tk.W)  # This makes the entry widget expand horizontally
 
tk.Label(root, text="Item:", bg='#5DA6C3').grid(row=2, sticky=tk.W)
item_entry = tk.Entry(root)
item_entry.grid(row=3, sticky=tk.E+tk.W)
 
tk.Label(root, text="Thirst amount:", bg='#5DA6C3').grid(row=4, sticky=tk.W)
hydration_scale = tk.Scale(root, from_=-10, to=20, resolution=1, orient=tk.HORIZONTAL)
hydration_scale.grid(row=5, sticky=tk.E+tk.W)
 
tk.Label(root, text="Quench Amount:", bg='#5DA6C3').grid(row=6, sticky=tk.W)
quenching_scale = tk.Scale(root, from_=-10, to=20, resolution=1, orient=tk.HORIZONTAL)
quenching_scale.grid(row=7, sticky=tk.E+tk.W)
 
# Create the add button
add_button = tk.Button(root, text="Add or Update Item", command=add_or_update_item, bg='green')
add_button.grid(row=8, sticky=tk.E+tk.W)
 
# Create the treeview
treeview = ttk.Treeview(root, columns=("Item ID", "Thirst Amount", "Quench Amount"), show='headings')
treeview.heading("Item ID", text="Item ID")
treeview.heading("Thirst Amount", text="Thirst Amount")
treeview.heading("Quench Amount", text="Quench Amount")
treeview.grid(row=9, sticky=tk.E+tk.W+tk.N+tk.S)  # This makes the treeview expand horizontally and vertically
treeview.bind('<<TreeviewSelect>>', load_item)  # Bind the load_item function to the treeview's select event
 
# Create the delete button
delete_button = tk.Button(root, text="Delete Item", command=delete_item, bg='red')
delete_button.grid(row=10, sticky=tk.E+tk.W)
 
# Create the "Common Items from Mods" menubutton
mods_menubutton = tk.Menubutton(root, text="Common Items from Mods", relief=tk.RAISED)
mods_menubutton.grid(row=11, sticky=tk.E+tk.W)
 
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

# Update the treeview with the existing items
update_treeview()
 
# Start the main loop
root.mainloop()
