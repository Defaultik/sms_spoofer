import os
import configparser

from vonage import Vonage, Auth
from vonage_sms import SmsMessage, SmsResponse
from vonage_account import Balance


config = configparser.ConfigParser()
config.read(os.path.join("data", "config.ini"))


def send_sms(number, sender, text):
    # Transmits user data to send sms
    auth = Auth(
        api_key=config["api_credentials"]["api_key"], 
        api_secret=config["api_credentials"]["api_secret"]
    )

    client = Vonage(auth=auth)

    message = SmsMessage(to=number, from_=sender, text=text, type="unicode")
    response: SmsResponse = client.sms.send(message)
    
    return response


def get_balance():
    auth = Auth(
        api_key=config["api_credentials"]["api_key"], 
        api_secret=config["api_credentials"]["api_secret"]
    )

    client = Vonage(auth=auth)

    balance: Balance = client.account.get_balance()

    return (f'{balance.value:0.2f} EUR')