import os
import configparser
import argparse
import vonage
from getpass import getpass


def main():
    global config

    parser = argparse.ArgumentParser(prog="SMS Spoofer", description="Fake the sender name and message content")
    parser.add_argument("-n", "--number", required=True, help="victim's phone number")
    parser.add_argument("-s", "--sender", required=True, help="sender name")
    parser.add_argument("-t", "--text", required=True, help="message content")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    if not os.path.exists("config.ini"):
        api_key = input("[!] Enter your Vonage API key: ")
        api_secret = getpass("[!] Enter your Vonage API Secret: ")

        config.add_section("api_credentials")

        config.set("api_credentials", "api_key", api_key)
        config.set("api_credentials", "api_secret", api_secret)

        with open("config.ini", "w") as config_file:
            config.write(config_file)

    config.read("config.ini")

    send_sms(args.number, args.sender, args.text)


def send_sms(number, sender, text):
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


if __name__ == "__main__":
    main()