import json, config

music_file = config.data_dir + 'music.json'

# Function to sort music tracks by score in descending order
def sort_tracks_by_score():
    try:
        # Read data from the JSON file
        with open(music_file, 'r') as file:
            data = json.load(file)

        # Sort the tracks by the 'score' parameter in descending order
        sorted_tracks = sorted(data, key=lambda x: x.get('score', 0), reverse=True)

        return sorted_tracks
    except FileNotFoundError:
        # Handle the case when the file is not found
        print("File '../wdata/music.json' not found.")
        return []
    except json.JSONDecodeError:
        # Handle JSON decoding errors
        print("Error decoding JSON data.")
        return []

# Function to like, dislike, unlike, or undislike a music track
def like_or_dislike_track(track_id, action):
    try:
        # Read data from the JSON file
        with open(music_file, 'r') as file:
            data = json.load(file)

        # Find the track with the specified ID
        for track in data:
            if track.get('id') == track_id:
                if action == 'like':
                    # Increase the track's score for a 'like'
                    track['score'] += 1
                elif action == 'dislike':
                    # Decrease the track's score for a 'dislike'
                    track['score'] -= 1
                elif action == 'unlike':
                    # Decrease the track's score for an 'unlike'
                    track['score'] -= 1
                elif action == 'undislike':
                    # Increase the track's score for an 'undislike'
                    track['score'] += 1

        # Write the updated data back to the file
        with open(music_file, 'w') as file:
            json.dump(data, file, indent=4)

        return 'ok'  # Return a success message

    except FileNotFoundError:
        # Handle the case when the file is not found
        print(f"File {music_file} not found.")
        return 'error: file not found'
    except json.JSONDecodeError:
        # Handle JSON decoding errors
        print("Error decoding JSON data.")
        return 'error: JSON decoding error'
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {str(e)}")
        return f'error: {str(e)}'

# Function to update the music JSON file with a new song entry
def update_music_json(new_song_entry):
    try:
        # Load the existing music data from the JSON file
        with open(music_file, 'r', encoding='utf-8') as json_file:
            music_data = json.load(json_file)

        # Generate a new ID for the song entry based on the length of the existing data
        new_song_id = str(len(music_data))

        # Add the new song entry to the music data
        new_song_entry['id'] = new_song_id
        music_data.append(new_song_entry)

        # Write the updated music data back to the JSON file
        with open(music_file, 'w', encoding='utf-8') as json_file:
            json.dump(music_data, json_file, ensure_ascii=False, indent=4)

        return new_song_id
    except Exception as e:
        # Handle any errors that may occur during the update process
        print(f"An error occurred while updating music data: {str(e)}")
        return None
