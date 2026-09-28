import os

# Path can be overridden (used by Docker so the file lives in a mounted volume)
INVENTORY_FILE = os.environ.get("INVENTORY_PATH", "inventory.txt")


def load_inventory():
    """Read total and history from the inventory file.

    File format:
        line 1: total units
        line 2: comma-separated transaction history (may be empty)

    If the file does not exist, start with an empty inventory.
    """
    if not os.path.exists(INVENTORY_FILE):
        print("No inventory file found. Starting with an empty inventory.")
        return 0, []

    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.read().splitlines()

        total = int(lines[0]) if lines and lines[0].strip() else 0
        history = []
        if len(lines) > 1 and lines[1].strip():
            history = [int(x) for x in lines[1].split(",")]

        print(f"Loaded inventory: total = {total}, {len(history)} past transactions.")
        return total, history
    except (ValueError, OSError):
        print("Inventory file unreadable. Starting with an empty inventory.")
        return 0, []


def save_inventory(total, history):
    """Write the final total and transaction history to the inventory file."""
    with open(INVENTORY_FILE, "w") as f:
        f.write(f"{total}\n")
        f.write(",".join(str(x) for x in history) + "\n")
    print(f"Inventory saved to {INVENTORY_FILE}")


def get_valid_input():
    value = input("Please enter stock quantity (or 'quit' to finish): ").strip()

    if value.lower() == "quit":
        return "quit"

    if not value.isdigit():
        print("  -> Error: please enter a whole number.")
        return None

    return int(value)


def process_delivery(total, new_value):
    return total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts, history):
    print("\n----- AUDIT REPORT -----")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed Attempts: {failed_attempts}")
    print(f"Transactions This Record: {len(history)}")
    print(f"Transaction History: {history}")
    print(f"Tax Owed (10%): {calculate_tax(total_units):.2f}")
    print("------------------------")


def main():
    total_units, history = load_inventory()
    failed_attempts = 0

    while True:
        result = get_valid_input()

        if result == "quit":
            break
        if result is None:
            failed_attempts += 1
            continue

        total_units = process_delivery(total_units, result)
        history.append(result)

    generate_report(total_units, failed_attempts, history)
    save_inventory(total_units, history)


if __name__ == "__main__":
    main()
