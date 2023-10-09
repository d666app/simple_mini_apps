import http.server
import socketserver
import hmac
import hashlib
import json
import os
from urllib.parse import unquote

import config
import bot
from pyapps import notes, minigame, wallet, music, casino

# Constants
PORT = config.PORT
public_dir = config.web_dir

# Allow reusing the address
socketserver.TCPServer.allow_reuse_address = True


def validate_hash(hash_str, init_data, token, c_str="WebAppData"):
    # Parse and sort the initialization data
    init_data = sorted([chunk.split("=")
                        for chunk in unquote(init_data).split("&")
                        if not chunk.startswith("hash=")],
                       key=lambda x: x[0])
    init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])

    # Generate the secret key and perform HMAC validation
    secret_key = hmac.new(c_str.encode(), token.encode(),
                         hashlib.sha256).digest()
    data_check = hmac.new(secret_key, init_data.encode(),
                          hashlib.sha256)

    return data_check.hexdigest() == hash_str


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/get_food':
            # Handle the '/get_food' endpoint
            response_data = json.loads(open('../wdata/order-food.json', 'r').readline())
            self.send_json_response(response_data)
        elif self.path == '/get-game-top':
            # Handle the '/get-game-top' endpoint
            response_data = minigame.get_game_top()
            self.send_json_response(response_data)
        elif self.path == '/get_music':
            # Handle the '/get_music' endpoint
            response_data = music.sort_tracks_by_score()
            self.send_json_response(response_data)
        else:
            file_extension = os.path.splitext(self.path)[1]
            if not file_extension:
                # Append '.html' to URLs that don't have an extension
                if self.path.endswith('/'):
                    self.path = self.path.rstrip('/') + '.html'
                else:
                    self.path += '.html'
            super().do_GET()


    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            if self.path in ("/get_data", "/new_note", "/delete_note", "/send-game-result", '/wallet_data','/casino_get','/casino_set'):
                post_data = self.rfile.read(content_length).decode("utf-8")
                bot_token = config.token
                data_dict = json.loads(post_data)
                data_check_string, received_hash, user_data = data_dict['data_str'], data_dict['hash'], data_dict['data']
                if validate_hash(received_hash, data_check_string, config.token, c_str="WebAppData"):
                    user_id = user_data['user']['id']
                    response_data = self.handle_api_request(self.path, user_id, data_dict)
                    self.send_json_response(response_data)
                else:
                    self.send_error_response("An error occurred while checking the data", 400)
            elif self.path == '/send_reaction':
                post_data = self.rfile.read(content_length).decode("utf-8")
                data_dict = json.loads(post_data)
                self.handle_reaction_request(data_dict)
            elif self.path == '/upload_mp3':
                self.handle_mp3_upload()
            else:
                super().do_GET()
        else:
            self.send_error_response("Bad Request: No data in the request body", 400)

    def handle_api_request(self, path, user_id, data_dict):
        # Handle various API endpoints
        response_data = {}

        if path == "/get_data":
            # Handle the '/get_data' endpoint
            user_notes = notes.get_or_create_user_data(user_id)
            response_data = {"list": user_notes}
        elif path == '/new_note':
            # Handle the '/new_note' endpoint
            text = data_dict['text']
            note_id = notes.add_note_to_user(user_id, text)
            response_data = {"id": str(note_id)}
        if path == "/casino_get":
            # Handle the '/casino_get' endpoint
            balance = casino.getbalance(user_id)
            response_data = {"balance": balance}
        elif path == '/casino_set':
            # Handle the '/casino_set' endpoint
            value = data_dict['value']
            note_id = casino.setbalance(user_id, value)
            response_data = {"status": 'ok'}
        elif path == '/delete_note':
            # Handle the '/delete_note' endpoint
            note_id = data_dict['id']
            user_notes = notes.remove_note_from_user(user_id, int(note_id))
            response_data = {"status": "Success"}
        elif path == "/send-game-result":
            # Handle the '/send-game-result' endpoint
            player_username = data_dict['data']['user'].get('username', 'Anon')
            score = data_dict['score']
            result = minigame.send_game_result(user_id, player_username, score)
            response_data = {"result": result}
        elif path == "/wallet_data":
            # Handle the '/wallet_data' endpoint
            value = data_dict.get('value')
            getter = data_dict.get('getter')
            response_data = wallet.create_user_wallet(user_id, getter, value)

        return response_data


    def handle_reaction_request(self, data_dict):
        track_id = data_dict.get('trackId')
        action = data_dict.get('action')

        if track_id and action:
            # Call the music.like_or_dislike_track function with the track_id and action
            result = music.like_or_dislike_track(track_id, action)

            # Create a response dictionary (you can customize this)
            response_data = {"result": result}
            self.send_json_response(response_data)
        else:
            # Handle the case where track_id or action is missing in the request data
            self.send_error_response("Invalid request data", 400)

    def handle_mp3_upload(self):
        try:
            content_length = int(self.headers.get('Content-length'))
            post_data = self.rfile.read(content_length)

            # Get form fields for artist and songTitle
            form_data = self.parse_mp3_upload_form(post_data)

            if 'musicFile' in form_data:
                # Save the MP3 file to the 'songs' directory
                new_song_id = music.update_music_json({
                    'songer': form_data.get('artist', ''),
                    'name': form_data.get('songTitle', ''),
                    'score': 0  # Initial score for the new song
                })

                mp3_filename = f'../public/songs/{new_song_id}.mp3'
                with open(mp3_filename, 'wb') as mp3_file:
                    mp3_file.write(form_data['musicFile'])

                # Respond with success message and the new song ID
                response_data = {
                    'status': 'success',
                    'message': 'MP3 file uploaded and song entry created successfully',
                    'new_song_id': new_song_id
                }

                self.send_json_response(response_data)
            else:
                # Handle the case where 'musicFile' is missing in the request
                self.send_error_response("Invalid request data", 400)
        except Exception as e:
            # Handle any other exceptions that may occur
            error_message = f"An error occurred: {str(e)}"
            self.send_error_response(error_message, 500)

    def parse_mp3_upload_form(self, post_data):
        form_data = {}
        boundary = self.headers.get('Content-Type').split('=')[1]
        sections = post_data.split(b'--' + boundary.encode())
        for section in sections:
            if b'name="artist"' in section:
                header, content = section.split(b'\r\n\r\n', 1)
                artist = content.decode()
                form_data['artist'] = artist

            if b'name="songTitle"' in section:
                header, content = section.split(b'\r\n\r\n', 1)
                songTitle = content.decode()
                form_data['songTitle'] = songTitle

            if b'filename="' in section:
                header, content = section.split(b'\r\n\r\n', 1)
                filename = header.split(b'filename="')[1].split(b'"')[0].decode()

                form_data['musicFile'] = content

        return form_data

    def send_json_response(self, data):
        # Send a JSON response
        response_json = json.dumps(data)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response_json.encode("utf-8"))

    def send_error_response(self, error_message, status_code):
        # Send an error response with a plain text message
        self.send_response(status_code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(error_message.encode("utf-8"))


with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
    print(f"Serving on port {PORT} from directory '{public_dir}'...")
    os.chdir(public_dir)
    httpd.serve_forever()
