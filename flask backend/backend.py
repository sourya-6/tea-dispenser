# flask_backend/app.py
import cv2.data
from flask import Flask, request, jsonify
# from pymongo import MongoClient
import cv2
import numpy as np
import base64
import os
from flask_cors import CORS
import face_recognition
from datetime import datetime
import pytz
import json
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# mongo_uri="mongodb+srv://karthikmoduguri:123@cluster0.pfo1j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(mongo_uri)

# db = client['backend']



# Directory to store user data
USERS_DIR = 'users'

# Ensure the users directory exists
if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load all encodings at startup for performance
def load_all_encodings():
    encodings = []
    user_ids = []
    for user_folder in os.listdir(USERS_DIR):
        user_path = os.path.join(USERS_DIR, user_folder)
        encoding_path = os.path.join(user_path, 'encoding.npy')
        if os.path.exists(encoding_path):
            stored_encoding = np.load(encoding_path)
            encodings.append(stored_encoding)
            # Extract user_id from folder name, e.g., 'user_1' -> '1'
            user_id = user_folder.split('_')[1]
            user_ids.append(user_id)
    return encodings, user_ids

known_encodings, known_user_ids = load_all_encodings()

# Helper function: Encode face using face_recognition library
def encode_face(image, face_coords):
    x, y, w, h = face_coords
    face_image = image[y:y+h, x:x+w]
    # Convert to RGB as face_recognition uses RGB images
    rgb_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    # Use face_recognition to get face encodings
    encodings = face_recognition.face_encodings(rgb_face)
    if len(encodings) > 0:
        return encodings[0]  # Return the first encoding found
    else:
        return None

# Helper function: Recognize face by comparing encodings with stored data
def recognize_face(encoding):
    min_distance = float('inf')
    recognized_user_id = None

    for idx, stored_encoding in enumerate(known_encodings):
        distance = np.linalg.norm(stored_encoding - encoding)
        if distance < min_distance:
            min_distance = distance
            recognized_user_id = known_user_ids[idx]

    # Define a threshold for recognition
    if min_distance < 0.5:
        return recognized_user_id
    else:
        return None

# Route for detecting and recognizing a face
@app.route('/detect-and-recognize', methods=['POST'])
def detect_and_recognize():
    try:
        data = request.get_json()
        image_data = data['image']
        #print(image_data)
        # Decode the base64 image
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(image_bytes,np.uint8)
        #print(nparr)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return jsonify({"success": False, "message": "No face detected."}), 200

        # Handle the first detected face
        face_coords = faces[0]
        encoding = encode_face(img, face_coords)

        if encoding is None:
            return jsonify({"success": False, "message": "Face encoding failed."}), 200

        # Recognize the face
        user_id = recognize_face(encoding)

        if user_id:
            # Load preferences
            user_folder = f'user_{user_id}'
            preferences_path = os.path.join(USERS_DIR, user_folder, 'preferences.json')
            if os.path.exists(preferences_path):
                with open(preferences_path, 'r') as f:
                    preferences = json.load(f)
            else:
                preferences = {}

            # Update last visited time
            metadata_path = os.path.join(USERS_DIR, user_folder, 'metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {}

            metadata['last_visited'] = datetime.now(pytz.utc).isoformat()
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f)

            return jsonify({
                "success": True,
                "recognized": True,
                "user": {
                    "id": user_id,
                    "name": user_folder.replace('user_', ''),
                    "teaPreferences": preferences,
                    "lastVisited": metadata.get('last_visited', '')
                }
            }), 200
        else:
            return jsonify({
                "success": True,
                "recognized": False,
                "message": "User not recognized. Please register."
            }), 200

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Error processing image."}), 500

# Route for registering a new user with face encoding and tea preferences
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        image_data = data['image']
        name = data['name']
        tea_preferences = data.get('teaPreferences', {
            "teaType": "Green",
            "sugarLevel": "Medium",
            "milk": "No"
        })

        # Create a unique user folder
        existing_users = [folder for folder in os.listdir(USERS_DIR) if folder.startswith('user_')]
        user_number = len(existing_users) + 1
        user_folder = f'user_{user_number}'
        user_path = os.path.join(USERS_DIR, user_folder)
        os.makedirs(user_path)

        # Decode the base64 image
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert to grayscale for detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            # Remove the created folder if no face detected
            os.rmdir(user_path)
            return jsonify({"success": False, "message": "No face detected."}), 200

        # Handle the first detected face
        face_coords = faces[0]
        encoding = encode_face(img, face_coords)

        if encoding is None:
            # Remove the created folder if encoding failed
            os.rmdir(user_path)
            return jsonify({"success": False, "message": "Face encoding failed."}), 200

        # Save the face image
        image_path = os.path.join(user_path, 'image.jpg')
        cv2.imwrite(image_path, img)

        # Save the face encoding
        encoding_path = os.path.join(user_path, 'encoding.npy')
        np.save(encoding_path, encoding)

        # Save the tea preferences
        preferences_path = os.path.join(user_path, 'preferences.json')
        with open(preferences_path, 'w') as f:
            json.dump(tea_preferences, f)

        # Save metadata
        metadata_path = os.path.join(user_path, 'metadata.json')
        metadata = {
            "last_visited": datetime.now(pytz.utc).isoformat()
        }
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)

        # Update known_encodings and known_user_ids
        known_encodings.append(encoding)
        known_user_ids.append(str(user_number))

        return jsonify({
            "success": True,
            "message": "User registered successfully.",
            "user": {
                "id": user_number,
                "name": name,
                "teaPreferences": tea_preferences,
                "lastVisited": metadata['last_visited']
            }
        }), 201

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Error processing image."}), 500

# Route for updating tea preferences of an existing user
@app.route('/update-preferences', methods=['POST'])
def update_preferences():
    try:
        data = request.get_json()
        user_id = data['user_id']
        tea_preferences = data.get('teaPreferences', {
            "teaType": "Green",
            "sugarLevel": "Medium",
            "milk": "No"
        })

        user_folder = f'user_{user_id}'
        user_path = os.path.join(USERS_DIR, user_folder)

        if not os.path.exists(user_path):
            return jsonify({"success": False, "message": "User does not exist."}), 404

        # Update preferences
        preferences_path = os.path.join(user_path, 'preferences.json')
        with open(preferences_path, 'w') as f:
            json.dump(tea_preferences, f)

        # Update last visited time
        metadata_path = os.path.join(user_path, 'metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {}

        metadata['last_visited'] = datetime.now(pytz.utc).isoformat()
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)

        return jsonify({
            "success": True,
            "message": "Tea preferences updated successfully.",
            "teaPreferences": tea_preferences,
            "lastVisited": metadata['last_visited']
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Error updating preferences."}), 500

# Route for updating tea preferences of an existing user
# @app.route('/update-preferences', methods=['POST'])
# def update_preferences():
#     try:
#         data = request.get_json()
#         user_id = data['user_id']
#         new_preference = data.get('teaPreferences', {
#             "teaType": "Green",
#             "sugarLevel": "Medium",
#             "milk": "No"
#         })

#         user_folder = f'user_{user_id}'
#         user_path = os.path.join(USERS_DIR, user_folder)

#         if not os.path.exists(user_path):
#             return jsonify({"success": False, "message": "User does not exist."}), 404

#         # Load existing preferences
#         preferences_path = os.path.join(user_path, 'preferences.json')
#         if os.path.exists(preferences_path):
#             print(preferences_path)
#             with open(preferences_path, 'r') as f:
#                 preferences_data = json.load(f)
#                 print(preferences_data)
#                 if "history" not in preferences_data or not isinstance(preferences_data["history"], list):
#                         preferences_data["history"] = []
#         else:
#             preferences_data = {"history": []}
#         print("hi")
#         # Append the new preference to the history
#         print(new_preference)
#         preferences_data["history"].append({
#             "preference": new_preference,
#             "timestamp": datetime.now(pytz.utc).isoformat()

#         })
#         # print(new_preference)
#         # Save updated preferences history
#         with open(preferences_path, 'w') as f:
#             json.dump(preferences_data, f)

#         # Update last visited time
#         metadata_path = os.path.join(user_path, 'metadata.json')
#         if os.path.exists(metadata_path):
#             with open(metadata_path, 'r') as f:
#                 metadata = json.load(f)
#         else:
#             metadata = {}

#         metadata['last_visited'] = datetime.now(pytz.utc).isoformat()
#         with open(metadata_path, 'w') as f:
#             json.dump(metadata, f)

#         # Find the most frequently chosen preference
#         preference_count = {}
#         for entry in preferences_data["history"]:
#             pref_str = json.dumps(entry["preference"])  # Convert preference to a string to count
#             if pref_str in preference_count:
#                 preference_count[pref_str] += 1
#             else:
#                 preference_count[pref_str] = 1

#         # Get the most frequently chosen preference
#         most_frequent_pref_str = max(preference_count, key=preference_count.get)
#         most_frequent_preference = json.loads(most_frequent_pref_str)

#         return jsonify({
#             "success": True,
#             "message": "Tea preferences updated successfully.",
#             "teaPreferences": {
#                 "lastPreference": new_preference,
#                 "mostFrequentPreference": most_frequent_preference
#             },
#             "lastVisited": metadata['last_visited']
#         }), 200

#     except Exception as e:
#         print(e)
#         return jsonify({"success": False, "message": "Error updating preferences."}), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)