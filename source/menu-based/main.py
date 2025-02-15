import configparser
import os
import csv

from api import send_sms, get_balance


BANNER = r"""
   ___ __  __ ___     ___ ___  ___   ___  ___ ___ ___  
  / __|  \/  / __|   / __| _ \/ _ \ / _ \| __| __| _ \ 
  \__ \ |\/| \__ \   \__ \  _/ (_) | (_) | _|| _||   / 
  |___/_|  |_|___/   |___/_|  \___/ \___/|_| |___|_|_\ 
"""


def print_options(*args):
    # Print a list of options
    for i, name in enumerate(args):
        print(f"[{i + 1}]", name)


def init():
    # Checks if we have all needed files in directory, and if not - creates them;
    # Starts program cycle
    global config

    config = configparser.ConfigParser()

    if not os.path.exists("data"):
        os.makedirs("data")
    
    contacts_path = os.path.join("data", "contacts.csv")
    config_path = os.path.join("data", "config.ini")

    if not os.path.exists(contacts_path):
        with open(contacts_path, "w", newline="") as contacts_file:
            writer = csv.DictWriter(contacts_file, fieldnames=("name", "phone_number"))
            writer.writeheader()

    if not os.path.exists(config_path):
        api_key = input("Enter your Vonage API key: ")
        api_secret = input("Enter your Vonage API Secret: ")

        config.add_section("api_credentials")
        config.set("api_credentials", "api_key", api_key)
        config.set("api_credentials", "api_secret", api_secret)

        with open(config_path, "w") as config_file:
            config.write(config_file)

    config.read(config_path)

    main()


def main():
    display_menu()
    print(f"Thank you for using!\nfrom https://github.com/Defaultik with <3")


def display_menu():
    # Main Menu Display
    while True:
        print("=" * 56)
        print(BANNER)
        print(f"{" " * 10}Your remaining balance is {get_balance()}")
        print("=" * 56)

        print_options("Single", "Multiple", "Contacts", "API Credentials", "Exit")
        selected_option = input("Enter number of the task: ")
        print("=" * 56)
        match selected_option:
            case "1":
                dial_number()
            case "2":
                dial_numbers()
            case "3":
                open_contacts()
            case "4":
                change_api_credentials()
            case "5":
                break
            case _:
                print("ERROR: Invalid option, try again")


def dial_number():
    # Send SMS to a single number menu
    number = input("Victim number: ").replace("+", "").replace("-", "").replace(" ", "") # removing pluses and spaces for VonageAPI that accepts only integer number
    sender = input("Sender name: ")
    text = input("Text: ")

    send_sms(number, sender, text)
    print("\nMessage sent successfully!")


def dial_numbers():
    # Send SMS to multiple numbers menu
    print("How many victims?")
    print_options("All of contacts", "Manual", "Back")
    selected_option = input("Enter number of the task: ")
    print("=" * 56)

    numbers = []
    match selected_option:
        case "1":
            with open(os.path.join("data", "contacts.csv"), "r") as contacts_file:
                reader = csv.DictReader(contacts_file)
                for row in list(reader):
                    numbers.append(row["phone_number"])
        case "2":
            count = int(input("How many numbers do you want to bulk: "))
            for i in range(count):
                number = input(f"Victim number #{i + 1}: ").replace("+", "").replace("-", "").replace(" ", "")
                numbers.append(number)
        case "3":
            return
        case _:
            print("ERROR: Invalid option")
            return

    print()
    sender = input("Sender name: ")
    text = input("Text: ")

    for number in numbers:
        send_sms(number, sender, text)


def open_contacts():
    # Contact management (new contacts creation, send to contact sms)
    with open(os.path.join("data", "contacts.csv"), "r") as contacts_file:
        reader = csv.DictReader(contacts_file)
        for i, row in enumerate(reader):
            print(f"[{i + 1}]", row["name"])

    print("\n[*] Create a new contact")
    print("[X] Back")

    task = input("\nEnter number of the task: ")
    print("=" * 56)
    match task:
        case "*":
            new_contact()
        case "x" | "X":
            return
        case _:
            try:
                select_num = int(task) - 1
                with open(os.path.join("data", "contacts.csv"), "r") as contacts_file:
                    reader = csv.DictReader(contacts_file)
                    rows = list(reader)

                number = rows[select_num]["phone_number"]
                print()
                sender = input("Sender name: ")
                text = input("Text: ")
                
                send_sms(number, sender, text)
            except (ValueError, IndexError):
                print("ERROR: Invalid option")
                return


def new_contact():
    # New contacts creation menu
    contact_name = input("\nContact name: ")
    contact_number = input("Contact number: ").replace("+", "").replace("-", "").replace(" ", "") # removing pluses and spaces for VonageAPI which accepts only integer number
        
    with open(os.path.join("data", "contacts.csv"), "a", newline = "") as contacts_file:
        writer = csv.DictWriter(contacts_file, fieldnames=("name", "phone_number"))
        writer.writerow({"name": contact_name, "phone_number": contact_number})


def change_api_credentials():
    # Change API credentials menu
    sure = input("Are you sure you want to change API Credentials (Y/N): ")
    if (sure.lower() == "y"): # did in in .lower() cuz we need to check any 'y' (small and large)
        api_key = input("\nEnter your new Vonage API key: ")
        api_secret = input("Enter your new Vonage API Secret: ")

        config.set("api_credentials", "api_key", api_key)
        config.set("api_credentials", "api_secret", api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)
        
        config.read("config.ini")


if __name__ == "__main__":
    init()