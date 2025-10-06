from datetime import datetime

class Item:
    def __init__(self, name, quantity, expiry):
        self.name = name
        self.quantity = quantity
        self.expiry = expiry

class Action:
    def __init__(self, index, previous_state):
        self.index = index
        self.previous_state = previous_state

inventory = []
action_history = []

def is_expired(expiry_date, current_date):
    return expiry_date < current_date
def is_valid_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def display_inventory():
    print("\nItem Name                         Quantity        Expiry Date")
    print("--------------------------- ----------------------------------")
    for item in inventory:
        print(f"{item.name:<35} {item.quantity:<15} {item.expiry}")

def check_low_stock():
    print("\n⚠️ Items with low stock (<=5):")
    found = False
    for item in inventory:
        if item.quantity <= 5:
            print(f"{item.name} - Qty: {item.quantity}, Expiry: {item.expiry}")
            found = True
    if not found:
        print("No low stock items.")

def add_item():
    if len(inventory) == 100:
        print("Inventory full.")
        return

    name = input("Enter item name (no spaces): ")
    expiry = input("Enter expiry date (YYYY-MM-DD): ")

    while not is_valid_date(expiry):
        print("Invalid date. Enter again.")
        expiry = input("Enter expiry date (YYYY-MM-DD): ")

    for i, item in enumerate(inventory):
        if item.name == name and item.expiry == expiry:
            qty = int(input("Product with same expiry exists. Enter quantity to add: "))
            action = Action(i, inventory[i])
            action_history.append(action)
            inventory[i].quantity += qty
            print(f"✅ Quantity updated. Total now: {inventory[i].quantity}")
            if inventory[i].quantity <= 5:
                print("⚠️ ALERT: Still low stock!")
            return

    quantity = int(input("Enter quantity (0-100): "))
    new_item = Item(name, quantity, expiry)
    inventory.append(new_item)
    action = Action(len(inventory)-1, new_item)
    action_history.append(action)
    print("✅ New item added.")
    if quantity <= 5:
        print("⚠️ ALERT: Low stock!")
    
def update_item():
    name = input("Enter item name to update: ")
    expiry = input("Enter expiry date to update (YYYY-MM-DD): ")

    found = False
    for i, item in enumerate(inventory):
        if item.name == name and item.expiry == expiry:
            action = Action(i, inventory[i])
            action_history.append(action)
            inventory[i].quantity = int(input("Enter new quantity (0-100): "))
            inventory[i].expiry = input("Enter new expiry date (YYYY-MM-DD): ")

            while not is_valid_date(inventory[i].expiry):
                print("Invalid date. Enter again.")
                inventory[i].expiry = input("Enter new expiry date (YYYY-MM-DD): ")

            print("✅ Item updated successfully!")
            if inventory[i].quantity <= 5:
                print("⚠️ ALERT: Low stock after update!")
            found = True
            break
    
    if not found:
        print("Item not found.")

def check_expiry():
    current_date = input("Enter current date (YYYY-MM-DD): ")

    print("\nExpired or near expiry items:")
    found = False
    for item in inventory:
        if is_expired(item.expiry, current_date):
            print(f"{item.name} (Expired: {item.expiry})")
            found = True
    if not found:
        print("No expired items.")

def undo_last_action():
    if not action_history:
        print("No actions to undo.")
        return
    
    last = action_history.pop()
    inventory[last.index] = last.previous_state
    print(f"✅ Last action undone: Restored {inventory[last.index].name} to previous state.")

def prepopulate_items():
    inventory.append(Item("Paracetamol", 10, "2025-12-01"))
    inventory.append(Item("Ibuprofen", 3, "2025-10-15"))
    inventory.append(Item("BandAid", 5, "2025-08-01"))
    print("Initial items added.")

def main():
    prepopulate_items()
    
    while True:
        print("\n===== MediTrack Inventory System =====")
        print("1. Display Inventory")
        print("2. Add Item")
        print("3. Update Item")
        print("4. Check Low Stock")
        print("5. Check Expiry")
        print("6. Undo Last Action")
        print("0. Exit")
        choice = int(input("Choose: "))
        
        if choice == 1:
            display_inventory()
        elif choice == 2:
            add_item()
        elif choice == 3:
            update_item()
        elif choice == 4:
            check_low_stock()
        elif choice == 5:
            check_expiry()
        elif choice == 6:
            undo_last_action()
        elif choice == 0:
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
