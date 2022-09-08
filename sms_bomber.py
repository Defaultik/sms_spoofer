import os
import platform
import csv
import configparser

from os import system

try:
    import vonage
    import psutil
except ImportError:
    os.system("pip install vonage")
    os.system("pip install psutil")

try:
    import vonage
    import psutil
except:
    pass

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def getProcess(name):
    for proc in psutil.process_iter():
        try:
            if name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False

if platform.system() == "Windows" and getProcess("excel.exe"):
    os.system("taskkill /im excel.exe")

config = configparser.ConfigParser()
try:
    open("config.ini")
    open("contacts.csv")

    config.read("config.ini")
except FileNotFoundError:
    clear()

    api_key = input("Type your API Key: ")
    api_secret = input("Type your API Secret: ")

    config.add_section("api_credentials")
    config.set("api_credentials", "api_key", api_key)
    config.set("api_credentials", "api_secret", api_secret)

    with open("config.ini", "w") as config_file:
        config.write(config_file)
    
    config.read("config.ini")

    with open("contacts.csv", "w") as contacts_file:
        fieldnames = ["name", "phone_number"]

        writer = csv.DictWriter(contacts_file, fieldnames = fieldnames)
        writer.writeheader()

client = vonage.Client(key = config["api_credentials"]["api_key"], secret = config["api_credentials"]["api_secret"])
sms = vonage.Sms(client)

def send_sms(name, number, text, count):
    for x in range(count):
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
    sender_name = input("Sender name: ")
    victim_number = input("Victim number: ").replace("+", "").replace(" ", "")

    sms_text = input("Text of SMS: ")
    sms_count = int(input("How much SMS do you want to send: "))

    send_sms(sender_name, victim_number, sms_text, sms_count)

def contacts():
    clear()

    with open("contacts.csv", "r") as contacts_file:
        reader = csv.DictReader(contacts_file)

        for i, row in enumerate(reader):
            print(f"[{i + 1}]", row["name"])

    print("\n[*] Create a new contact")
    print("[M] Back to Main menu")

    select = input("\nSelect task and press Enter: ")

    if select == "*":
        contact_creating()
    elif select.lower() == "m":
        menu()
    else:
        with open("contacts.csv", "r") as contacts_file:
            reader = csv.DictReader(contacts_file)
            rows = list(reader)

        sender_name = input("Sender name: ")

        select_num = int(select) - 1
        victim_number = rows[select_num]["phone_number"]

        sms_text = input("Text of SMS: ")
        sms_count = int(input("How much SMS do you want to send: "))

        send_sms(sender_name, victim_number, sms_text, sms_count)

        menu()

def contact_creating():
    contact_name = input("\nContact name: ")
    contact_number = input("Contact number: ").replace("+", "").replace(" ", "")
        
    with open("contacts.csv", "a", newline = "") as contacts_file:
        fieldnames = ["name", "phone_number"]

        writer = csv.DictWriter(contacts_file, fieldnames = fieldnames)
        writer.writerow({"name": contact_name, "phone_number": contact_number})

    contacts()

def change_api_credentials():
    api_key = input("\nType your new API Key: ")
    api_secret = input("Type your new API Secret: ")
        
    config.set("api_credentials", "api_key", api_key)
    config.set("api_credentials", "api_secret", api_secret)

    with open("config.ini", "w") as config_file:
        config.write(config_file)
    
    config.read("config.ini")

    menu()

def menu():
    clear()

    print("[1] Phone number")
    print("[2] Contacts")
    print("[3] Change API credentials")

    menu_select = input("\nSelect task and press Enter: ")

    if menu_select == "1":
        dial_number()
    elif menu_select == "2":
        contacts()
    elif menu_select == "3":
        change_api_credentials()
    else:
        menu()

if __name__ == "__main__":
    menu()