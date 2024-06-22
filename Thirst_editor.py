import tkinter as tk
from tkinter import ttk, messagebox
import json
import webbrowser
import subprocess
import os
import re
import tomli

def create_settings_file():
    export_window = tk.Toplevel()
    export_window.title("Export File Name")
    export_window.geometry('405x45')
    inputtxt = tk.Text(export_window, height = 1, width = 50)
    # inputtxt.grid(column=0, row=0, sticky="news")
    inputtxt.pack(side="top", fill='x', expand=True)
    file_name = ""
    def fileNameGet():
        subprocess.run(["python", "Generate_item_settings_file.py", inputtxt.get(1.0, "end-1c")])
    buttons = tk.Frame(export_window)
    # buttons.grid(column=0, row=1, sticky=tk.N+tk.W)
    buttons.pack(side = "bottom", fill='x', expand=True)
    button_close = tk.Button(buttons, text = "Save", command=lambda : [fileNameGet(), export_window.destroy()], width = 10, padx = 2)
    button_cancel = tk.Button(buttons, text = "Cancel", command=lambda : [export_window.destroy()], width = 10, padx=2)
    button_close.grid(column=0, row=0, sticky=tk.N+tk.W)
    button_cancel.grid(column=1, row=0, sticky=tk.N+tk.W, padx = 5)
    
    # Call the Python script

    
# Initialize the list
item_list = []

def load_items():
    # Initialize the items list
    items = []

    # Load the items from the food file
    try:
        with open('items.json', 'r') as f:
            for item in json.load(f):
                items.append(item)
    except FileNotFoundError:
        pass  # If the file doesn't exist, do nothing

    return items

def add_or_update_item():
    # Get the values from the entry fields
    modid = modid_entry.get()
    item = '_'.join(item_entry.get().lower().split())
    hydration = hydration_scale.get()
    quenching = quenching_scale.get()

    # Combine the modid and item to form the item-id
    item_id = f"{modid}:{item}"

    # Load the existing items from the file
    try:
        with open('items.json', 'r') as f:
            existing_items = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        existing_items = []

    # Check if the item already exists in the list
    for i, existing_item in enumerate(existing_items):
        if existing_item[0] == item_id:
            # Update the existing item
            existing_items[i] = [item_id, hydration, quenching, item_type.get()]
            break
    else:
        # Add the new item to the list
        existing_items.append([item_id, hydration, quenching, item_type.get()])
    # Save the list to the appropriate file based on the selected item type
    with open('items.json', 'w') as f:
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

    item_list.remove(treeview.item(selected_item)['values'])

    # Save the list to a file
    with open('items.json', 'w') as f:
        json.dump(item_list, f)

    # Update the treeview
    update_treeview()

def delete_all_item():
    # Delete the selected item from the list

    item_list.clear()

    # Save the list to a file
    with open('items.json', 'w') as f:
        json.dump(item_list, f)

    # Update the treeview
    update_treeview()


def update_treeview(*args):
    global item_list
    if args:
        treeview.delete(*treeview.get_children())
        for item in item_list:
            if args[0] in item[0]:
                treeview.insert('', 'end', values=item)
        root.update_idletasks()
        return


    # Load the items from the food and drink files
    try:
        with open('items.json', 'r') as f:
            item_list = json.load(f).copy()
    except FileNotFoundError:
        item_list = []

    # Clear the current items in the treeview
    treeview.delete(*treeview.get_children())

    # Add each item in the food and drink items to the treeview
    for item in item_list:
        treeview.insert('', 'end', values=item)

    # Force the UI to update
    root.update_idletasks()

def load_item(event):
    # Get the selected item
    selected_item = treeview.selection()

    # Check if an item is selected
    if not selected_item:
        return

    # Load the values into the entry fields
    item_id, hydration, quenching, item_type = treeview.item(selected_item[0])['values']
    modid, item = item_id.split(":")
    item = ' '.join(map(lambda s: s[0].upper() + s[1:], item.replace('_', ' ').split()))
    modid_entry.delete(0, tk.END)
    modid_entry.insert(0, modid)
    item_entry.delete(0, tk.END)
    item_entry.insert(0, item)
    hydration_scale.set(hydration)
    quenching_scale.set(quenching)
    if (item_type == 'food'):
        food_button.invoke()
    else:
        drink_button.invoke()



def set_item(itemTuple):
    # global food_button, drink_button
    # Set the values of the entry fields
    item_id, hydration, quenching, item_type = itemTuple
    modid, item = item_id.split(":")
    item = ' '.join(map(lambda s: s[0].upper() + s[1:], item.replace('_', ' ').split()))
    modid_entry.delete(0, tk.END)
    modid_entry.insert(0, modid)
    item_entry.delete(0, tk.END)
    item_entry.insert(0, item)
    hydration_scale.set(hydration)
    quenching_scale.set(quenching)
    if (item_type == 'food'):
        food_button.invoke()
    else:
        drink_button.invoke()

def addAll(modName):
    for item in menus[modName]:
        set_item(item)
        add_or_update_item()
        modid_entry.delete(0, tk.END)
        item_entry.delete(0, tk.END)
        hydration_scale.set(0)
        quenching_scale.set(0)

# Load the existing items
item_list = load_items()

# Create the main window
root = tk.Tk()
root.title("Azureddraig's Thirst was Taken Helper")  # Set the title of the window
root.geometry("900x700")  # Set the window size
# root.grid_columnconfigure(0, weight=1)  # Allows column to stretch upon resizing
root.configure(bg='#5DA6C3')  # Set the background color

# Create the labels and entry fields
# tk.Label(root, text="Mod:", bg='#5DA6C3').grid(row=0, column=0, sticky=tk.W)
tk.Label(root, text="Mod:", bg='#5DA6C3').pack(side='top', anchor='w')
modid_entry = tk.Entry(root)
# modid_entry.grid(row=1, column=0, sticky="news")  # This makes the entry widget expand horizontally
modid_entry.pack(side='top', fill='x', expand=True)  # This makes the entry widget expand horizontally

# tk.Label(root, text="Item:", bg='#5DA6C3').grid(row=2, column=0, sticky=tk.W)
tk.Label(root, text="Item:", bg='#5DA6C3').pack(side='top', anchor='w')
item_entry = tk.Entry(root)
item_entry.pack(side='top', fill='x', expand=True)

tk.Label(root, text="Thirst amount:", bg='#5DA6C3').pack(side='top', anchor='w')
hydration_scale = tk.Scale(root, from_=-20, to=20, resolution=1, orient=tk.HORIZONTAL)
hydration_scale.pack(side='top', fill='x', expand=True)

tk.Label(root, text="Quench Amount:", bg='#5DA6C3').pack(side='top', anchor='w')
quenching_scale = tk.Scale(root, from_=-20, to=20, resolution=1, orient=tk.HORIZONTAL)
quenching_scale.pack(side='top', fill='x', expand=True)


# Create the radio buttons for item type
item_type = tk.StringVar(value='food')
item_type_frame = tk.Frame(root)
item_type_frame.pack(side = 'top', anchor='w', pady=4)
food_button = tk.Radiobutton(item_type_frame, text='Food', variable=item_type, value='food')
food_button.pack()
drink_button = tk.Radiobutton(item_type_frame, text='Drink', variable=item_type, value='drink')
drink_button.pack()

#Create modification frames
modify_frame = tk.Frame(root)
modify_frame.pack(side= 'top', fill ='x', expand=True)
# Create the add button
add_button = tk.Button(modify_frame, text="Add or Update Item", command=add_or_update_item, bg='green')
add_button.pack(side='top', fill='x', expand=True)

# Create the "Common Items from Mods" menubutton
mods_menubutton = tk.Menubutton(modify_frame, text="Common Items from Mods", relief=tk.RAISED)
mods_menubutton.pack(side='top', fill='x', expand=True)
 
# Create the "Common Items from Mods" menu
mods_menu = tk.Menu(mods_menubutton, tearoff=0)
mods_menubutton.configure(menu=mods_menu)
 
# Create the mod menus

# Look into configs folder, record the name of the toml files: remember this name, formatted by removing underscores and replacing with ' ', 
# put into hashmap values with key being the name and the values being a list of item+thirst.
# Upon finishing the parsing for the entire configs folder, construct the menus as follow:
# For each mod name recorded, create a menu attached to mods_menu: for each [name]: newMod_menu = tk.Menu(...); mods_menu.add_cascade(label="[name]", menu = newMod_menu)
# Within each of these sub-menus, attach new menus representing individual consumable items onto. for each item in map[name]: newMod_menu.add_command(label = format(item[0]), command=set_item(item))

cwd = os.getcwd()
config_dir = os.path.join(cwd, "Compat Library")
print(os.listdir(config_dir))
menus = dict()
for fileName in os.listdir(config_dir):
    newMenuName = re.search(r'(.*).toml', fileName).group(1).replace('_', ' ')
    # menus[newMenuName]
    with open(os.path.join(config_dir, fileName), 'rb') as f:
        mod_dict = tomli.load(f)
        menus[newMenuName] = []
        for drink in mod_dict['Drinks']['drinks']:
            menus[newMenuName].append(drink + ['drink'])
        for food in mod_dict['Foods']['foods']:
            menus[newMenuName].append(food + ['food'])
mods_menu_dict = {}
for mod in menus:
    mods_menu_dict[mod] = tk.Menu(mods_menu, tearoff = 0)
    mods_menu.add_cascade(label = mod, menu = mods_menu_dict[mod])
    mods_menu_dict[mod].add_command(label = f'Add all from {mod}', command=lambda modName=mod: [addAll(modName)])
    for ind_item in menus[mod]:
        modId, itemName = ind_item[0].split(':')
        label = ' '.join(map(lambda s: s[0].upper() + s[1:], itemName.replace('_', ' ').split()))
        mods_menu_dict[mod].add_command(label = label, command=lambda item=ind_item: [set_item(item)])
    

# Create the delete button
delete_button = tk.Button(modify_frame, text="Delete Item", command=delete_item, bg='orange')
delete_button.pack(side='top', fill='x', expand=True)

# Create the delete all button
delete_button = tk.Button(modify_frame, text="Delete All Items", command=delete_all_item, bg='red')
delete_button.pack(side='top', fill='x', expand=True)




# Create the search label and entry field
tk.Label(root, text="Search:", bg='#5DA6C3').pack(side='top')
search_var = tk.StringVar()
search_var.trace_add('write', lambda *args: update_treeview(search_var.get()))
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(side='top', fill='x', expand=True)



# Create a frame
frame = tk.Frame(root)
frame.pack(side='top', fill='both', expand=True)

# Configure the grid to expand
# root.grid_rowconfigure(15, weight=1)  # Only the row containing the frame will expand
# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)

# Create the treeview inside the frame with an additional "Item Type" column
treeview = ttk.Treeview(frame, columns=("Item ID", "Thirst Amount", "Quench Amount", "Item Type"), show='headings')
treeview.heading("Item ID", text="Item ID")
treeview.heading("Thirst Amount", text="Thirst Amount")
treeview.heading("Quench Amount", text="Quench Amount")
treeview.heading("Item Type", text="Item Type")  # New column header
treeview.pack(fill=tk.BOTH, expand=True)  # This makes the treeview expand horizontally and vertically within the frame

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

for col in ["Item ID", "Thirst Amount", "Quench Amount", "Item Type"]:
    treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))


# Create a scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)

# Configure the treeview to use the scrollbar
treeview.configure(yscrollcommand=scrollbar.set)

# Pack the treeview and the scrollbar
treeview.pack(side="left", fill=tk.BOTH, expand=True)
scrollbar.pack(side="right", fill="y")

treeview.bind('<<TreeviewSelect>>', load_item)  # Bind the load_item function to the treeview's select event

# Create the settings
create_button = tk.Button(root, text="Create Settings file", command=create_settings_file, bg='#99ccff')
create_button.pack(side='bottom', fill='x', expand=True)

# Update the treeview with the existing items
update_treeview()
 
# Start the main loop
root.mainloop()
