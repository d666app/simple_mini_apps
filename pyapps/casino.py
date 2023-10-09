import os, config
file_path = config.data_dir +'casino/'

def getbalance(id):
    user_path = file_path + f'/{id}'
    # Check if the file exists
    if os.path.exists(user_path):
        # If the file exists, read its contents
        with open(user_path, 'r') as file:
            balance = int(file.read())
    else:
        # If the file doesn't exist, create it and write the initial value
        with open(user_path, 'w') as file:
            file.write('1000')
        balance = 1000

    return balance

def setbalance(id, value):
    user_path = file_path + f'/{id}'

    # Write the new value to the file
    with open(user_path, 'w') as file:
        file.write(str(value))
