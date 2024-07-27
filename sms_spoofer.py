import os
import sys
import csv
import configparser
import vonage
from time import sleep


def clear():
    # Function to clear the terminal on both Unix-like and Windows systems
    if (sys.platform == "win32"):
        os.system("cls")
    else:
        os.system("clear")


def print_options(*args):
    # Print a list of options
    for i, name in enumerate(args):
        print(f"[{i + 1}]", name)


def main():
    # Function that checks if we have all needed files in directory, and if not - creates them
    global config

    config = configparser.ConfigParser()
    
    if not os.path.exists("contacts.csv"):
        with open("contacts.csv", "w", newline="") as contacts_file:
            writer = csv.DictWriter(contacts_file, fieldnames=("name", "phone_number"))
            writer.writeheader()

    if not os.path.exists("config.ini"):
        api_key = input("Enter your Vonage API key: ")
        api_secret = input("Enter your Vonage API Secret: ")

        config.add_section("api_credentials")

        config.set("api_credentials", "api_key", api_key)
        config.set("api_credentials", "api_secret", api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)

    config.read("config.ini")

    while True:
        sleep(1)
        menu()


def menu():
    # Function to display the main menu
    clear()

    print("Welcome to the SMS Spoofer")
    print("SMS Spoofer is made in educational purposes")
    print("\nby Defaultik\n")

    print_options("Phone Number", "Bulk", "Contacts", "Change API credentials", "Exit")
    selected_tab = input("Enter number of the task: ")
    match selected_tab:
        case "1":
            dial_number()
        case "2":
            bulk_numbers()
        case "3":
            open_contacts()
        case "4":
            change_api_credentials()
        case "5":
            exit()
        case _:
            print("ERROR: Invalid option, try again")
            return


def send_sms(number, sender, text):
    # Function to send SMS
    client = vonage.Client(
        key=config["api_credentials"]["api_key"],
        secret=config["api_credentials"]["api_secret"]
    )

    sms = vonage.Sms(client)
    response_data = sms.send_message({
        "from": sender,
        "to": number,
        "text": text,
        "type": "unicode"
    })

    if response_data["messages"][0]["status"] == "0":
        print("\nMessage sent successfully.")
    else:
        print(f"\nMessage failed with error: {response_data['messages'][0]['error-text']}")


def dial_number():
    # Function to send SMS to a single number
    number = input("\nVictim number: ").replace("+", "").replace(" ", "") # removing pluses and spaces for VonageAPI that accepts only integer number
    sender = input("Sender name: ")
    text = input("Text of the SMS: ")

    send_sms(number, sender, text)


def bulk_numbers():
    # Function to send SMS to multiple numbers
    clear()

    print_options("All of contacts", "Manual")
    bulk_type = input("Enter number of the task: ")

    numbers = []
    match bulk_type:
        case "1":
            with open("contacts.csv", "r") as contacts_file:
                reader = csv.DictReader(contacts_file)
                for row in list(reader):
                    numbers.append(row["phone_number"])
        case "2":
            count = int(input("\nHow many numbers do you want to bulk: "))
            for i in range(count):
                number = input(f"Victim number #{i + 1}: ").replace("+", "").replace(" ", "")
                numbers.append(number)
        case _:
            print("ERROR: Invalid option")
            return

    sender = input("Sender name: ")
    text = input("Text of the SMS: ")

    for number in numbers:
        send_sms(number, sender, text)


def open_contacts():
    # Function to manage contacts
    clear()

    with open("contacts.csv", "r") as contacts_file:
        reader = csv.DictReader(contacts_file)
        for i, row in enumerate(reader):
            print(f"[{i + 1}]", row["name"])

    print("\n[*] Create a new contact")
    print("[X] Cancel")

    task = input("\nEnter number of the task: ")
    match task:
        case "*":
            new_contact()
        case "x" | "X":
            menu()
        case _:
            try:
                select_num = int(task) - 1
                with open("contacts.csv", "r") as contacts_file:
                    reader = csv.DictReader(contacts_file)
                    rows = list(reader)

                number = rows[select_num]["phone_number"]
                sender = input("Sender name: ")
                text = input("Text of the SMS: ")
                
                send_sms(number, sender, text)
            except (ValueError, IndexError):
                print("ERROR: Invalid option, try again")
                sleep(1)
                open_contacts()


def new_contact():
    # Function to create a new contact
    contact_name = input("\nContact name: ")
    contact_number = input("Contact number: ").replace("+", "").replace(" ", "") # removing pluses and spaces for VonageAPI which accepts only integer number
        
    with open("contacts.csv", "a", newline = "") as contacts_file:
        writer = csv.DictWriter(contacts_file, fieldnames=("name", "phone_number"))
        writer.writerow({"name": contact_name, "phone_number": contact_number})


def change_api_credentials():
    # Function to change API credentials
    sure = input("Are you sure you want to change API Credentials (Y/N): ")
    if (sure.lower() == "y"): # did in in .lower() cuz we need to check any 'y' (small and large)
        api_key = input("\nEnter your new Vonage API key: ")
        api_secret = input("Enter your new Vonage API Secret: ")

        config.set("api_credentials", "api_key", api_key)
        config.set("api_credentials", "api_secret", api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)
        
        config.read("config.ini")


def check_python_version():
    # Check if the Python version is appropriate
    if sys.version_info < (3, 10):
        print("ERROR: Inappropriate Python version!\nFor proper functioning of the program, you should install Python 3.10 or higher.")
        return False
    
    return True


if __name__ == "__main__":
    if check_python_version():
        main()

# SMS Spoofer by Defaultik
# https://github.com/Defaultik