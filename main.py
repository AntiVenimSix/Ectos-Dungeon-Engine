import json
import time
import random
import sys

# Initialize Dungeon variables and lists
editormode = False
debug = False
dungeon = []
editingRoom = {}
items = []
enemies = []
itemdata = {}
enemydata = {}

# Initialize Player
inventory = {}
life = 95
maxlife = 100
action = ""
currentRoom = 0
equipped_item = None

# Function to create an enemy
def createEnemy(mindamage, maxdamage, hp, name):
    enemydata = {"name": name, "mindamage": mindamage, "maxdamage": maxdamage, "hp": hp}
    enemies.append(enemydata)

# Function to create an item
def createItem(damage, idnum, name):
    itemdata = {"damage": damage, "idnum": idnum, "name": name}
    items.append(itemdata)

# Function to create a room
def createRoom(desc, item, doors, enemy):  # doors should be a list of room ids
    editingRoom = {"desc": desc, "item": item, "doors": doors, "enemies": enemy}
    dungeon.append(editingRoom)

# Function to save dungeon to a JSON file
def createDungeon():
    data = {
        "dungeon": dungeon,
        "items": items,
        "enemies": enemies
    }
    with open('name.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Level saved")

def decideAction(action):
    global currentRoom, life, inventory, equipped_item

    room = dungeon[currentRoom]

    if action == "1":  # Get Item
        if room["item"]:
            item = room["item"]
            inventory[item["idnum"]] = item
            print(f"You picked up {item['name']}.")
            room["item"] = None
        else:
            print("No items in this room.")
    
    elif action == "2":  # Fight
        if room["enemies"]:
            for enemy in list(room["enemies"]):
                print(f"Fighting {enemy['name']} (HP: {enemy['hp']}, Damage: {enemy['mindamage']}-{enemy['maxdamage']})")
                while enemy['hp'] > 0 and life > 0:
                    player_damage = random.randint(4, 6)
                    if equipped_item:
                        player_damage += equipped_item["damage"]
                    enemy['hp'] -= player_damage
                    print(f"You hit the {enemy['name']} for {player_damage} damage!")
                    if enemy['hp'] <= 0:
                        print(f"You defeated the {enemy['name']}!")
                        room["enemies"].remove(enemy)
                        break
                    enemy_damage = random.randint(enemy['mindamage'], enemy['maxdamage'])
                    life -= enemy_damage
                    print(f"The {enemy['name']} hits you for {enemy_damage} damage!")
                    if life <= 0:
                        print("You have been defeated! Game over!")
                        sys.exit()
            # After fight, heal player
            life = min(life + 10, maxlife)
            print(f"Health restored! Current health: {life}/{maxlife}")
        else:
            print("No enemies in this room to fight.")
    
    elif action == "3":  # Enter Door
        if room["doors"]:
            next_room = random.choice(room["doors"])  # Choose a random door
            if 0 <= next_room < len(dungeon):
                print(f"You enter room {next_room}.")
                currentRoom = next_room
            else:
                print("That door seems to be blocked.")
        else:
            print("There are no doors in this room.")
    
    elif action == "4":  # Equip Item
        if inventory:
            print("Your Inventory:")
            for item in inventory.values():
                print(f"{item['name']} (Damage: {item['damage']})")
            equip_item = input("Enter item name to equip: ")
            for item in inventory.values():
                if item["name"] == equip_item:
                    equipped_item = item
                    print(f"You equipped {equip_item}.")
                    break
            else:
                print("That item is not in your inventory.")
        else:
            print("No items in your inventory.")
    
    elif action == "5":  # Check Health
        print(f"Your health: {life}/{maxlife}")
    
    elif action == "6":  # View Inventory
        if inventory:
            print("Your Inventory:")
            for item in inventory.values():
                print(f"{item['name']} (Damage: {item['damage']})")
        else:
            print("Your inventory is empty.")

# Function to describe the room
def describeRoom():
    room = dungeon[currentRoom]
    print(f"Room {currentRoom}: {room['desc']}")
    
    if room["item"]:
        print(f"Item in this room: {room['item']['name']}")
    else:
        print("No items in this room.")
    
    if room["enemies"]:
        print("Enemies in this room:")
        for enemy in room["enemies"]:
            print(f"- {enemy['name']} (HP: {enemy['hp']}, Damage: {enemy['mindamage']}-{enemy['maxdamage']})")
    
    print(f"Health: {life}/{maxlife}")
    print("Actions: 1: Get Item | 2: Fight | 3: Enter Door | 4: Equip Item | 5: Check Health | 6: View Inventory")
    action = input("What do you want to do? (1, 2, 3, 4, 5, or 6): ")
    return action

def load_dungeon(path):
    print("Loading dungeon")
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        dungeon_data = data["dungeon"]
        item_data = data["items"]
        enemy_data = data["enemies"]
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print(f"Failed to load dungeon data: {error}")
        sys.exit(1)

    print("Loaded! Extracting data...")
    return dungeon_data, item_data, enemy_data


def main():
    global dungeon, items, enemies

    print("You're using Ecto's Dungeon Generator version 0.1.0 Alpha! Please support me by subscribing to my YouTube channel @EctoPhasic and @PhasiCat!")

    # If in editor mode, create dungeon and save
    if editormode:
        createDungeon()
        print("Dungeon file generated! Closing in 5 seconds...")
        time.sleep(5)
        sys.exit()

    dungeon, items, enemies = load_dungeon('example.json')

    print("Done! Finishing up...")
    if debug:
        print("Dungeon:", dungeon)
        print("Items:", items)
        print("Enemies:", enemies)

    # Main game loop
    while True:
        action = describeRoom()
        decideAction(action)


if __name__ == "__main__":
    main()
