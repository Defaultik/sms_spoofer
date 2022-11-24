import os
import sys
import csv
import configparser
import platform

try:
    import vonage
except ImportError:
    os.system("pip install vonage")
finally:
    import vonage

config = configparser.ConfigParser()


def main():
    try:
        open("config.ini")
        config.read("config.ini")

        open("contacts.csv")
    except FileNotFoundError:
        vonage_api_key = input("[!] Type your Vonage API key: ")
        vonage_api_secret = input("[!] Type your Vonage API Secret: ")

        config.add_section("api_credentials")
        config.set("api_credentials", "api_key", vonage_api_key)
        config.set("api_credentials", "api_secret", vonage_api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)

        config.read("config.ini")

        fieldnames = ["name", "phone_number"]
        with open("contacts.csv", "w", newline="") as contacts_file:
            writer = csv.DictWriter(contacts_file, fieldnames=fieldnames)
            writer.writeheader()


def clear():
    if (sys.platform == "win32"):
        os.system("cls")
    else:
        os.system("clear")


def menu():
    clear()

    menu_tabs = ["Phone Number", "Contacts", "Change API credentials", "Exit"]

    print("Welcome to SMS Spoofer!")
    for i, name in enumerate(menu_tabs):
        print(f"[{i + 1}]", name)
    
    selected_tab = input("\nSelect task and press Enter: ")

    if (selected_tab == "1"):
        dial_number()
    elif (selected_tab == "2"):
        contacts()
    elif (selected_tab == "3"):
        change_api_credentials()
    elif (selected_tab == "4"):
        raise SystemExit


def send_sms(name, number, text):
    client = vonage.Client(
        key = config["api_credentials"]["api_key"],
        secret = config["api_credentials"]["api_secret"]
    )

    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": name,
            "to": number,
            "text": text,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("SMS sent successfully.")
    else:
        print(f"SMS failed with error: {responseData['messages'][0]['error-text']}")


def dial_number():
    sms_victim_number = input("\nVictim number: ")

    sms_sender_name = input("Sender name: ")
    sms_text = input("Text of SMS: ")

    send_sms(sms_sender_name, sms_victim_number, sms_text)


def contacts():
    clear()

    with open("contacts.csv", "r") as contacts_file:
        reader = csv.DictReader(contacts_file)

        for i, row in enumerate(reader):
            print(f"[{i + 1}]", row["name"])

    print("\n[*] Create a new contact")
    print("[X] Cancel")

    contacts_select_task = input("\nSelect task and press Enter: ")

    if (contacts_select_task == "*"):
        new_contact()
    else:
        with open("contacts.csv", "r") as contacts_file:
            reader = csv.DictReader(contacts_file)
            rows = list(reader)

        select_num = int(contacts_select_task) - 1

        sms_sender_name = input("Sender name: ")

        sms_victim_number = rows[select_num]["phone_number"]
        sms_text = input("Text of SMS: ")

        send_sms(sms_sender_name, sms_victim_number, sms_text)


def new_contact():
    contact_name = input("\nContact name: ")
    contact_number = input("Contact number: ").replace("+", "").replace(" ", "")
        
    with open("contacts.csv", "a", newline = "") as contacts_file:
        fieldnames = ["name", "phone_number"]

        writer = csv.DictWriter(contacts_file, fieldnames = fieldnames)
        writer.writerow({"name": contact_name, "phone_number": contact_number})

    contacts()


def change_api_credentials():
    sure = input("[?] Are you sure you want to change API Credentials (y/n): ")

    if (sure.lower() == "y"):
        vonage_api_key = input("\n[!] Type your Vonage API key: ")
        vonage_api_secret = input("[!] Type your Vonage API Secret: ")

        config.set("api_credentials", "api_key", vonage_api_key)
        config.set("api_credentials", "api_secret", vonage_api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)
        
        config.read("config.ini")


if __name__ == "__main__":
    main()

    while True:
        Menu = menu()