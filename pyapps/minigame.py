import json,config

top_file_dir = config.data_dir + 'mini-game-top.json'

# Function to get the top 20 scores
def get_game_top():
    try:
        # Read the existing top scores from the file
        with open(top_file_dir, 'r') as file:
            top_scores = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist yet, initialize with an empty list
        top_scores = []

    # Sort the top scores by score (descending order) and take the top 20
    top_scores.sort(key=lambda x: x['score'], reverse=True)
    top_20_scores = top_scores[:20]

    return top_20_scores

# function for updating a player's result, as well as getting his actual results

def send_game_result(player_id, username, score):
    try:
        # Read the existing top scores from the file
        with open(top_file_dir, 'r') as file:
            top_scores = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist yet, initialize with an empty list
        top_scores = []

    # Check if the player's ID already exists in the top scores
    existing_entry = next((entry for entry in top_scores if entry['id'] == player_id), None)

    # Create a new score entry for the current player
    new_score_entry = {'id': player_id, 'username': username, 'score': score}

    if existing_entry:
        # Update the score if the player's ID already exists and the new score is higher
        if score > existing_entry['score']:
            existing_entry['score'] = score
    else:
        # Add the new score entry if the player's ID is not found or if the new score is higher
        top_scores.append(new_score_entry)

    # Sort the top scores by score (descending order)
    top_scores.sort(key=lambda x: x['score'], reverse=True)

    # Write the updated top scores back to the file
    with open(top_file_dir, 'w') as file:
        json.dump(top_scores, file)

    # Get the best result (top score) of the given player
    player_best_result = next((entry for entry in top_scores if entry['id'] == player_id), None)

    return player_best_result
