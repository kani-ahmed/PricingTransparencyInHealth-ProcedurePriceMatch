# user_views.py
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import UserPreference, Notification, User, ChatbotMessage
from flask_cors import cross_origin

user_view = Blueprint('user_view', __name__)


def register_user_routes(app):
    @app.route('/register', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def register_user():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')  # Assuming the front end sends this

        if User.query.filter((User.username == username) | (User.email == email)).first():
            # User already exists
            return jsonify({"error": "Username or email already in use"}), 409

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201

    # TESTING PURPOSES ONLY

    @app.route('/get_password/<int:user_id>', methods=['GET'])
    def get_password(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Return the password (not recommended for production)
        return jsonify({"password": user.password_hash}), 200

    @app.route('/set_password/<int:user_id>', methods=['POST'])
    def set_user_password(user_id):
        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({"error": "Password not provided"}), 400

        # Fetch the user by user id
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Generate a hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Set the hashed password for the user
        user.password_hash = hashed_password

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Password set successfully"}), 200

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Retrieve the user from the database based on the provided username/email
        user = User.query.filter((User.username == username) | (User.email == username)).first()

        if user and check_password_hash(user.password_hash, password):
            # Passwords match, user is authenticated
            # Generate a JWT token or session token and return it to the client for future authenticated requests
            return jsonify({"message": "Login successful", "user_id": user.id}), 200
        else:
            # Invalid credentials
            return jsonify({"error": "Invalid username/email or password"}), 401

    @app.route('/update_preferences/<int:user_id>', methods=['PUT'])
    def update_preferences(user_id):
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update user preferences
        preferences = UserPreference.query.filter_by(user_id=user_id).first()
        if not preferences:
            preferences = UserPreference(user_id=user_id)
            db.session.add(preferences)

        preferences.receive_notifications = data.get('receive_notifications', preferences.receive_notifications)
        preferences.privacy_settings = data.get('privacy_settings', preferences.privacy_settings)
        db.session.commit()

        return jsonify({"message": "Preferences updated successfully"}), 200

    @app.route('/get_notifications/<int:user_id>', methods=['GET'])
    def get_notifications(user_id):
        notifications = Notification.query.filter_by(user_id=user_id).all()
        notifications_data = [{"id": n.id, "content": n.content, "is_read": n.is_read,
                               "timestamp": n.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for n in notifications]
        return jsonify(notifications_data), 200

    @app.route('/view_profile/<int:user_id>', methods=['GET'])
    def view_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        profile_data = {
            "username": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture,
            "eco_points": user.eco_points
        }

        # Optional: include additional user data, like preferences
        preferences = UserPreference.query.filter_by(user_id=user_id).first()
        if preferences:
            profile_data["preferences"] = {
                "receive_notifications": preferences.receive_notifications,
                "privacy_settings": preferences.privacy_settings
            }

        return jsonify(profile_data), 200

    @app.route('/update_user_profile/<int:user_id>', methods=['PUT'])
    def update_user_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.json
        user.profile_picture = data.get('profile_picture', user.profile_picture)
        # Update additional fields as needed

        db.session.commit()

        return jsonify({"message": "User profile updated successfully"}), 200

    @app.route('/get_chatbot_messages/<int:user_id>', methods=['GET'])
    def get_chatbot_messages(user_id):
        messages = ChatbotMessage.query.filter_by(user_id=user_id).order_by(ChatbotMessage.timestamp).all()
        message_data = [{"id": m.id, "content": m.content, "timestamp": m.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                         "message_type": m.message_type} for m in messages]
        return jsonify(message_data), 200

    @app.route('/add_chatbot_message', methods=['POST'])
    def add_chatbot_message():
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')
        message_type = data.get('message_type')

        if not user_id or not content or not message_type:
            return jsonify({"error": "Missing required fields"}), 400

        new_message = ChatbotMessage(user_id=user_id, content=content, message_type=message_type)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({"message": "Chatbot message added successfully"}), 201
