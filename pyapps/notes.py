import os
import json
import config

# Get the absolute path of the script's directory
parent_dir = os.path.dirname(os.path.abspath(__file__))

# Define the directory where user data files will be stored
user_data_dir = config.data_dir +'notes/'

# Function to get or create user data
def get_or_create_user_data(user_id):
    # Construct the path to the user's data file
    user_data_file = os.path.join(user_data_dir, f'{user_id}.json')

    if os.path.exists(user_data_file):
        # If the file exists, read its content
        with open(user_data_file, 'r') as file:
            try:
                user_data = json.load(file)
            except json.JSONDecodeError:
                # Handle JSON decoding errors by returning an empty dictionary
                user_data = {}
    else:
        # If the file doesn't exist, create a new one and write an empty dictionary
        user_data = {'notes': []}
        os.makedirs(user_data_dir, exist_ok=True)
        with open(user_data_file, 'w') as file:
            json.dump(user_data, file)

    # Return the 'notes' list from the user's data
    return user_data['notes']

# Function to add a note to a user's data
def add_note_to_user(user_id, text):
    # Construct the path to the user's data file
    user_data_file = os.path.join(user_data_dir, f'{user_id}.json')

    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            try:
                user_data = json.load(file)
            except json.JSONDecodeError:
                user_data = {"notes": []}
    else:
        user_data = {"notes": []}

    # Find the maximum note ID from existing notes, if any
    max_id = max([note.get("id", -1) for note in user_data["notes"]], default=-1)

    # Increment the ID by 1 to create a new note
    new_id = max_id + 1

    # Create a new note
    new_note = {"id": new_id, "text": text}

    # Add the new note to the existing notes
    user_data["notes"].append(new_note)

    # Write the updated data to the user's data file
    with open(user_data_file, 'w') as file:
        json.dump(user_data, file)

    # Return the ID of the newly created note
    return new_id

# Function to remove a note from a user's data by ID
def remove_note_from_user(user_id, note_id):
    # Construct the path to the user's data file
    user_data_file = os.path.join(user_data_dir, f'{user_id}.json')

    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            try:
                user_data = json.load(file)
            except json.JSONDecodeError:
                user_data = {"notes": []}
    else:
        user_data = {"notes": []}

    # Find the index of the note with the specified ID
    note_index = None
    for i, note in enumerate(user_data["notes"]):
        if note.get("id") == note_id:
            note_index = i
            break

    if note_index is not None:
        # Remove the note by index
        del user_data["notes"][note_index]
        # Write the updated data to the user's data file
        with open(user_data_file, 'w') as file:
            json.dump(user_data, file)
        return True  # Note successfully removed
    else:
        return False  # Note with the specified ID not found
