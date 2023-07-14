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
    
config = configparser.ConfigParser()


# wrote function to clear terminal on both types of systems (unix-like and windows)
def clear():
    if (sys.platform == "win32"):
        os.system("cls")
    else:
        os.system("clear")


# my shitty function about checking if string is english or another language
def is_latin(string):
    return string.isalpha() and string.isascii()


# function that checks if we have all needed files in directory, and if we don't - create them
def main():
    try:
        open("config.ini")
        config.read("config.ini")
    except FileNotFoundError:
        vonage_api_key = input("Enter your Vonage API key: ")
        vonage_api_secret = input("Enter your Vonage API Secret: ")

        config.add_section("api_credentials")

        config.set("api_credentials", "api_key", vonage_api_key)
        config.set("api_credentials", "api_secret", vonage_api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)

        config.read("config.ini")

    try:
        open("contacts.csv")
    except FileNotFoundError:
        with open("contacts.csv", "w", newline="") as contacts_file:
            writer = csv.DictWriter(contacts_file, fieldnames=("name", "phone_number"))
            writer.writeheader()


def menu():
    clear()

    print("\nWelcome to the SMS Spoofer!")
    print("SMS Spoofer is made in educational purposes")
    print("\nby Defaultik\n")

    # i just like this method where computer writes all of menu tabs instead of you :)
    menu_tabs = (
        "Phone Number",
        "Contacts",
        "Change API credentials",
        "Exit"
    )

    for i, name in enumerate(menu_tabs): 
        print(f"[{i + 1}]", name)

    selected_tab = input("Enter your task: ")

    if (selected_tab == "1"):
        dial_number()
    elif (selected_tab == "2"):
        contacts()
    elif (selected_tab == "3"):
        change_api_credentials()
    elif (selected_tab == "4"):
        exit()


def send_sms(number, sender, text):
    client = vonage.Client(
        key = config["api_credentials"]["api_key"],
        secret = config["api_credentials"]["api_secret"]
    )

    sms = vonage.Sms(client)

    if (is_latin(text)): # did it because was report about problems with sending sms's on another languages (not english)
        responseData = sms.send_message(
            {
                "from": sender,
                "to": number,
                "text": text
            }
        )
    else:
        responseData = sms.send_message(
            {
                "from": sender,
                "to": number,
                "text": text,
                "type": "unicode"
            }
        )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


def dial_number():
    sms_victim_number = input("\nVictim number: ").replace("+", "").replace(" ", "") # removing pluses and spaces for VonageAPI which accepts only integer number

    sms_sender_name = input("Sender name: ")
    sms_text = input("Text of SMS: ")

    send_sms(sms_victim_number, sms_sender_name, sms_text)


def contacts():
    clear()

    with open("contacts.csv", "r") as contacts_file:
        reader = csv.DictReader(contacts_file)

        for i, row in enumerate(reader):
            print(f"[{i + 1}]", row["name"])

    print("\n[*] Create a new contact")
    print("[X] Cancel")

    contacts_select_task = input("\nEnter task: ")

    if (contacts_select_task == "*"):
        new_contact()
    elif (contacts_select_task.lower() == "x"): # did in in .lower() cuz we need to check any 'x' (small and large)
        pass
    else:
        with open("contacts.csv", "r") as contacts_file:
            reader = csv.DictReader(contacts_file)
            rows = list(reader)

        select_num = int(contacts_select_task) - 1

        sms_sender_name = input("Sender name: ")

        sms_victim_number = rows[select_num]["phone_number"]
        sms_text = input("Text of SMS: ")
        
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
# https://t.me/defaultiiik