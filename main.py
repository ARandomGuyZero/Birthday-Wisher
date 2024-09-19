"""
Birthday Wisher

Author: Alan
Date: September 19th, 2024

This project is a simple birthday wisher, that sends a happy birthday message if the current date coincides with the birthday's date.
"""

from smtplib import SMTP
from datetime import datetime
from pandas import read_csv
from random import choice

NAME = "Your name"
EMAIL = "Your email"
PASSWORD = "Your password"
HOST = "smtp.gmail.com" # I use gmail's smtp, may change depending on your email provider
PORT = 587

LETTER_TEMPLATES = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]

def get_birthday_data():
    """
    Gets the data of the birthday
    :return: Returns the csv data as a dictionary
    """
    # Open birthday data
    birthday_data = read_csv("birthdays.csv")
    return birthday_data.to_dict(orient="records")

def write_letter(recipient_name):
    """
    Writes a letter
    :param recipient_name: String with the name of who is receiving the message
    :return:
    """

    # Gets a random file path
    letter_path = "letter_templates/" + choice(LETTER_TEMPLATES)

    with open(letter_path, "r") as letter_template_file:
        letter_body = letter_template_file.read()

    # Replace some placeholders to make it feel unique
    new_letter = letter_body.replace("[NAME]", recipient_name)
    new_letter = new_letter.replace("[YOUR NAME]", NAME)

    return new_letter

def send_letter(recipient_email, letter_message):
    """
    Sends a letter to the email.
    :param recipient_email: String that has who is receiving the email
    :param letter_message: String that has the message
    :return:
    """
    with SMTP(host=HOST, port=PORT) as connection:
        # Starts the connection
        connection.starttls()

        # Login the account
        connection.login(user=EMAIL, password=PASSWORD)

        # Send the message
        connection.sendmail(from_addr=EMAIL, to_addrs=recipient_email, msg=f"Subject:Happy Birthday!\n\n{letter_message}")

# Get the birthday data
birthday_dict = get_birthday_data()

# Get today's date
today = datetime.now()

# Get today's date as a tuple for better reading
today_tuple = (today.month, today.day)

# For each birthday in the dictionary, we will check if the today's date is the same as the birthday date
for birthday in birthday_dict:

    # Get the birthday data
    name = birthday["name"]
    email = birthday["email"]

    # Get the birthday's date as a tuple
    birthday_tuple = (birthday["month"], birthday["day"])

    # Check if today's date is the same as the birthday
    if birthday_tuple == today_tuple:

        message = write_letter(name)
        send_letter(email, message)