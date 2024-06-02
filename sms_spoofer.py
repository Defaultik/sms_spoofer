# ordered imports, cuz in the first version of the program it was crazy
import os, sys, csv, configparser
from time import sleep


try:
    import vonage
except ImportError:
    install_confirm = input("ERROR: Vonage distributions wasn't found\nDo you want to install (Y/N): ") # added question if user wants to install library

    if (install_confirm.lower() == "y"):
        os.system("pip install vonage")
    else:
        exit()
finally:
    import vonage
    print("Loading...")


# function to clear terminal on both types of systems (unix-like and windows)
def clear():
    if (sys.platform == "win32"):
        os.system("cls")
    else:
        os.system("clear")


def print_options(options):
    for i, name in enumerate(options):
        print(f"[{i + 1}]", name)


# function that checks if we have all needed files in directory, and if we don't - create them
def main():
    global config

    config = configparser.ConfigParser()

    try:
        open("config.ini")
    except FileNotFoundError:
        vonage_api_key = input("Enter your Vonage API key: ")
        vonage_api_secret = input("Enter your Vonage API Secret: ")

        config.add_section("api_credentials")

        config.set("api_credentials", "api_key", vonage_api_key)
        config.set("api_credentials", "api_secret", vonage_api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)
    finally:
        config.read("config.ini")

    try:
        open("contacts.csv")
    except FileNotFoundError:
        with open("contacts.csv", "w", newline="") as contacts_file:
            writer = csv.DictWriter(contacts_file, fieldnames=("name", "phone_number"))
            writer.writeheader()


def menu():
    clear()

    print("Welcome to the SMS Spoofer!")
    print("SMS Spoofer is made in educational purposes")
    print("\nby Defaultik\n")

    print_options(("Phone Number", "Bulk", "Contacts", "Change API credentials", "Exit"))
    selected_tab = input("Enter your task: ")
    match selected_tab:
        case "1":
            dial_number()
        case "2":
            bulk()
        case "3":
            contacts()
        case "4":
            change_api_credentials()
        case "5":
            exit()


def send_sms(number, sender, text):
    client = vonage.Client(
        key = config["api_credentials"]["api_key"],
        secret = config["api_credentials"]["api_secret"]
    )

    sms = vonage.Sms(client)
    responseData = sms.send_message({
        "from": sender, 
        "to": number, 
        "text": text, 
        "type": "unicode"
    })

    if responseData["messages"][0]["status"] == "0":
        print("\nMessage sent successfully.")
    else:
        print(f"\nMessage failed with error: {responseData['messages'][0]['error-text']}")


def dial_number():
    sms_victim_number = input("\nVictim number: ").replace("+", "").replace(" ", "") # removing pluses and spaces for VonageAPI which accepts only integer number

    sms_sender_name = input("Sender name: ")
    sms_text = input("Text of the SMS: ")

    send_sms(sms_victim_number, sms_sender_name, sms_text)


def bulk():
    numbers = []

    bulk_type = input("Bulk all of your contacts | Manual (1/2): ")
    match bulk_type:
        case "1":
            with open("contacts.csv", "r") as contacts_file:
                reader = csv.DictReader(contacts_file)

                for row in list(reader):
                    numbers.append(row["phone_number"])
        case "2":
            numbers_count = int(input("\nHow many numbers do you want to bulk: "))

            for i in range(numbers_count):
                sms_victim_number = input("#%d Victim number: " % i + 1).replace("+", "").replace(" ", "")
                numbers.append(sms_victim_number)
        case _:
            menu()

    sms_sender_name = input("Sender name: ")
    sms_text = input("Text of the SMS: ")
    print()

    for i in numbers:
        send_sms(i, sms_sender_name, sms_text)


def contacts():
    clear()

    with open("contacts.csv", "r") as contacts_file:
        reader = csv.DictReader(contacts_file)

        for i, row in enumerate(reader):
            print(f"[{i + 1}]", row["name"])

    print("\n[*] Create a new contact")
    print("[X] Cancel")

    contacts_select_task = input("\nEnter task: ")
    match contacts_select_task:
        case "*":
            new_contact()
        case contacts_select_task if contacts_select_task.lower()  == "x":
            menu()
        case _:
            with open("contacts.csv", "r") as contacts_file:
                reader = csv.DictReader(contacts_file)
                rows = list(reader)

            select_num = int(contacts_select_task) - 1

            sms_sender_name = input("Sender name: ")
            sms_victim_number = rows[select_num]["phone_number"]
            sms_text = input("Text of the SMS: ")
            
            send_sms(sms_victim_number, sms_sender_name, sms_text)


def new_contact():
    contact_name = input("\nContact name: ")
    contact_number = input("Contact number: ").replace("+", "").replace(" ", "") # removing pluses and spaces for VonageAPI which accepts only integer number
        
    with open("contacts.csv", "a", newline = "") as contacts_file:
        writer = csv.DictWriter(contacts_file, fieldnames=("name", "phone_number"))
        writer.writerow({"name": contact_name, "phone_number": contact_number})


# just function that changes data in a file
def change_api_credentials():
    sure = input("Are you sure you want to change API Credentials (Y/N): ")
    if (sure.lower() == "y"): # did in in .lower() cuz we need to check any 'y' (small and large)
        vonage_api_key = input("\nEnter your Vonage API key: ")
        vonage_api_secret = input("Enter your Vonage API Secret: ")

        config.set("api_credentials", "api_key", vonage_api_key)
        config.set("api_credentials", "api_secret", vonage_api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)
        
        config.read("config.ini")


if __name__ == "__main__":
    main()

    while True: # putting menu in cycle to not call all the time menu(); also a sleep here so that the user can see the logs
        sleep(1)
        menu()


# SMS Spoofer by Defaultik
# https://github.com/Defaultik