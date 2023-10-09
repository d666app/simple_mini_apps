import requests
import json
import time
import multiprocessing
import config
import re


BASE_URL = f'https://api.telegram.org/bot{config.token}/'
site_domain = config.site_domain
# Create a bot session using the requests library
bot = requests.Session()
bot_username = ''
# Function to send a text message to a chat
def send_message(chat_id, text, keyboard=None):
    url = BASE_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': keyboard}
    response = bot.post(url, data=data)
    return response.json()

# Function to check the format of a domain
def is_valid_domain(domain):
    return re.match(r".+\..+", domain)
# Function to get information about the bot itself
def get_me(token):
    url = f'https://api.telegram.org/bot{token}/getMe'
    response = bot.post(url)
    return response.json()

# Function to handle incoming messages
def handle_message(update):
    chat_id = update['message']['chat']['id']
    message = update['message']
    if 'text' in message:
        text = message['text']

        if text == '/start':
            response_text = 'To use one of the applications, press the button 👇'
            webapp_keyboard = json.dumps({'inline_keyboard': [
                [{"text": "🧠 Notes", "url": f"https://t.me/{bot_username}/notes?startapp"},
                 {"text": "🎰 Casino", "url": f"https://t.me/{bot_username}/casino?startapp"}],
                [{"text": "🎧 Music", "url": f"https://t.me/{bot_username}/music?startapp"},
                 {"text": "👛 Wallet", "url": f"https://t.me/{bot_username}/wallet?startapp"}]
            ]})
            reply_keyboard = json.dumps({'keyboard': [[{"text": "Order food", "web_app": {"url": f"https://{site_domain}/order-food"}}]],
                                          "resize_keyboard": True})

            send_message(chat_id, '👋', reply_keyboard)
            send_message(chat_id, response_text, webapp_keyboard)
    elif 'web_app_data' in message:
        send_message(chat_id, message['web_app_data']['data'])
    else:
        print(update)

# Main function to receive updates and handle messages
def main():
    offset = None
    while True:
        url = BASE_URL + 'getUpdates'
        params = {'offset': offset, 'timeout': 30}
        response = bot.get(url, params=params)
        updates = response.json()['result']

        for update in updates:
            offset = update['update_id'] + 1
            handle_message(update)

# Check the bot token
while True:
    if not get_me(config.token)['ok']:
        user_token = input("Please enter your bot token: ")
        config.token = user_token
        BASE_URL = f'https://api.telegram.org/bot{config.token}/'
        try:
            if get_me(config.token)['ok']:
                with open('config.py', 'r') as config_file:
                    lines = config_file.readlines()

                with open('config.py', 'w') as config_file:
                    for line in lines:
                        if line.startswith("token = "):
                            config_file.write(f"token = '{config.token}'\n")
                        else:
                            config_file.write(line)
                break
            else:
                print("Invalid token. Please try again.")
        except Exception as e:
            print(f"Error checking token: {e}")
    else:
        break
bot_username = get_me(config.token)['result']['username']

# Check and request the website domain
while True:
    domain = input("Please enter the website domain: ")
    if is_valid_domain(domain):
        with open('config.py', 'r') as config_file:
            lines = config_file.readlines()

        with open('config.py', 'w') as config_file:
            for line in lines:
                if line.startswith("site_domain = "):
                    config_file.write(f"site_domain = '{domain}'\n")
                    site_domain = domain
                else:
                    config_file.write(line)
        break
    else:
        print("Invalid domain format. Please try again.")

# Start the bot in a separate process
bot_process = multiprocessing.Process(target=main)
bot_process.start()

