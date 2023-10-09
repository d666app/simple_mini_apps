import os
import json
import string
import random
import config
# Define constants
WALLET_DIR = config.data_dir+'wallet/'
WALLET_EXTENSION = '.json'
BALANCE_DEFAULT = 100

# Function to generate a unique wallet ID for a user
def generate_wallet_id(user_id):
    while True:
        wallet_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        wallet_file = os.path.join(WALLET_DIR, f'{user_id}-{wallet_id}{WALLET_EXTENSION}')
        if not os.path.exists(wallet_file):
            return wallet_id

# Function to create or manage a user's wallet
def create_user_wallet(user_id, getter=None, value=None):
    # Create the wallet directory if it doesn't exist
    if not os.path.exists(WALLET_DIR):
        os.makedirs(WALLET_DIR)

    # Check if the user already has a wallet
    user_wallet_files = [file for file in os.listdir(WALLET_DIR) if file.startswith(f'{user_id}-')]
    if user_wallet_files:
        wallet_file = os.path.join(WALLET_DIR, user_wallet_files[0])
        with open(wallet_file, 'r') as file:
            wallet_data = json.load(file)
        wallet_id = wallet_data.get('wallet_id')
        balance = wallet_data.get('balance')
    else:
        # Generate a unique wallet ID for the user
        wallet_id = generate_wallet_id(user_id)
        balance = BALANCE_DEFAULT

    # If a value is provided and the balance is sufficient, deduct it from the user's balance
    if value is not None:
        if balance >= value:
            if getter is not None:
                getter_wallet_files = [file for file in os.listdir(WALLET_DIR) if getter in file]
                if getter_wallet_files:
                    getter_wallet_file = os.path.join(WALLET_DIR, getter_wallet_files[0])
                    with open(getter_wallet_file, 'r') as file:
                        getter_wallet_data = json.load(file)
                    getter_balance = getter_wallet_data.get('balance')
                    getter_balance += value
                    balance -= value
                    getter_wallet_data = {
                        'wallet_id': getter_wallet_data.get('wallet_id'),
                        'balance': getter_balance
                    }
                    with open(getter_wallet_file, 'w') as file:
                        json.dump(getter_wallet_data, file)
                else:
                    return {"error": "Recipient not found"}
        else:
            return {"error": "Not enough balance"}

    # Save the updated wallet data to the user's wallet file
    wallet_data = {
        'wallet_id': wallet_id,
        'balance': balance
    }
    wallet_file = os.path.join(WALLET_DIR, f'{user_id}-{wallet_id}{WALLET_EXTENSION}')
    with open(wallet_file, 'w') as file:
        json.dump(wallet_data, file)

    return {
        "wallet_id": wallet_id,
        "balance": balance
    }
