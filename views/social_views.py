# social_views.py
from flask import request, jsonify, Blueprint

from extensions import db
from models import Post, Like, Comment, Friendship, User, MessagesInbox

social_view = Blueprint('social_view', __name__)


def register_social_routes(app):
    @app.route('/create_post', methods=['POST'])
    def create_post():
        user_id = request.json['user_id']
        content = request.json['content']

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_post = Post(user_id=user_id, content=content, created_at=db.func.current_timestamp())
        db.session.add(new_post)
        db.session.commit()

        return jsonify({"message": "Post created successfully", "post_id": new_post.id}), 201

    @app.route('/like_post/<int:post_id>/<int:user_id>', methods=['POST'])
    def like_post(post_id, user_id):
        if not Post.query.get(post_id) or not User.query.get(user_id):
            return jsonify({"error": "Post or user not found"}), 404

        like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
        if like:
            return jsonify({"error": "Already liked"}), 400

        new_like = Like(post_id=post_id, user_id=user_id)
        db.session.add(new_like)
        db.session.commit()

        return jsonify({"message": "Post liked successfully"}), 201

    @app.route('/add_comment', methods=['POST'])
    def add_comment():
        user_id = request.json['user_id']
        post_id = request.json['post_id']
        content = request.json['content']

        if not Post.query.get(post_id) or not User.query.get(user_id):
            return jsonify({"error": "Post or user not found"}), 404

        new_comment = Comment(post_id=post_id, user_id=user_id, content=content, timestamp=db.func.current_timestamp())
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({"message": "Comment added successfully"}), 201

    @app.route('/add_friend/<int:user_id>/<int:friend_id>', methods=['POST'])
    def add_friend(user_id, friend_id):
        if user_id == friend_id:
            return jsonify({"error": "Cannot add yourself as a friend"}), 400

        user = User.query.get(user_id)
        friend = User.query.get(friend_id)
        if not user or not friend:
            return jsonify({"error": "User or friend not found"}), 404

        existing_friendship = Friendship.query.filter(
            ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id)) |
            ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id))).first()
        if existing_friendship:
            return jsonify({"error": "Friendship already exists or request pending"}), 400

        new_friendship = Friendship(user_id=user_id, friend_id=friend_id, status="requested")
        db.session.add(new_friendship)
        db.session.commit()

        return jsonify({"message": "Friend request sent successfully"}), 201

    @app.route('/respond_friend_request/<int:user_id>/<int:friend_id>', methods=['POST'])
    def respond_friend_request(user_id, friend_id):
        data = request.get_json()
        action = data.get('action')  # Expecting 'accept' or 'decline'

        # Assuming the friend_id is the one who received the request and user_id is the one who sent it
        friendship = Friendship.query.filter_by(user_id=friend_id, friend_id=user_id, status="requested").first()
        if not friendship:
            return jsonify({"error": "Friend request not found"}), 404

        if action == "accept":
            friendship.status = "accepted"
        elif action == "decline":
            db.session.delete(friendship)
        else:
            return jsonify({"error": "Invalid action"}), 400

        db.session.commit()

        action_response = "accepted" if action == "accept" else "declined"
        return jsonify({"message": f"Friend request {action_response}"}), 200

    @app.route('/remove_friend/<int:user_id>/<int:friend_id>', methods=['DELETE'])
    def remove_friend(user_id, friend_id):
        # Check if there's a friendship or a friend request from user_id to friend_id
        friendship = Friendship.query.filter(
            ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id) &
             (Friendship.status.in_(["accepted", "requested"]))) |
            ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id) &
             (Friendship.status.in_(["accepted", "requested"])))
        ).first()

        if not friendship:
            return jsonify({"error": "Friendship or friend request not found"}), 404

        # If a "requested" friendship is found where the current user is the recipient, this implies declining the
        # request
        if friendship.status == "requested" and friendship.user_id == friend_id:
            action = "declined"
        else:
            # Otherwise, it's either canceling sent request or removing an accepted friendship
            action = "canceled" if friendship.status == "requested" else "removed"

        db.session.delete(friendship)
        db.session.commit()

        return jsonify({"message": f"Friend request {action} successfully"}), 200

    @app.route('/view_posts', methods=['GET'])
    def view_posts():
        # Fetch all posts along with user details via a join (this avoids an N+1 query problem)
        posts = Post.query.join(User).all()
        post_list = [{
            'post_id': post.id,
            'username': post.user.username,  # Accessing the username from the User model
            'content': post.content,
            'created_at': post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': post.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        } for post in posts]

        return jsonify(post_list), 200

    @app.route('/view_my_posts/<int:user_id>', methods=['GET'])
    def view_my_posts(user_id):
        # Ensure user exists
        if not User.query.get(user_id):
            return jsonify({"error": "User not found"}), 404

        # Fetch posts only for the specified user along with user details via a join
        posts = Post.query.join(User).filter(Post.user_id == user_id).all()
        post_list = [{
            'post_id': post.id,
            'username': post.user.username,
            'content': post.content,
            'created_at': post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': post.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        } for post in posts]

        return jsonify(post_list), 200

    @app.route('/get_users', methods=['GET'])
    def get_all_users():
        users = User.query.all()
        user_list = [{
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        } for user in users]

        return jsonify(user_list), 200

    @app.route('/get_friendships/<int:user_id>', methods=['GET'])
    def get_user_friendships(user_id):
        friendships = Friendship.query.filter(
            (Friendship.user_id == user_id) | (Friendship.friend_id == user_id)
        ).all()

        friendship_list = []
        for friendship in friendships:
            friend = User.query.get(friendship.friend_id if friendship.user_id == user_id else friendship.user_id)
            friendship_data = {
                'id': friendship.id,
                'user_id': user_id,
                'friend_id': friendship.friend_id if friendship.user_id == user_id else friendship.user_id,
                'friend_name': friend.username if friend else None,
                'status': friendship.status,
                'request_type': 'outgoing' if friendship.user_id == user_id else 'incoming',
                'created_at': friendship.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': friendship.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            friendship_list.append(friendship_data)

        return jsonify(friendship_list), 200

    # Send a message to another user
    @app.route('/send_message', methods=['POST'])
    def send_message():
        sender_id = request.json.get('sender_id')
        recipient_id = request.json.get('recipient_id')
        content = request.json.get('content')

        # Check if required fields are missing
        if not sender_id or not recipient_id or not content:
            return jsonify({'message': 'Missing required fields'}), 400

        # Check if sender and recipient users exist
        sender = User.query.get(sender_id)
        recipient = User.query.get(recipient_id)
        if not sender or not recipient:
            return jsonify({'message': 'Invalid sender or recipient'}), 400

        try:
            message = MessagesInbox(
                user_id=recipient_id,
                sender_id=sender_id,
                content=content
            )

            db.session.add(message)
            db.session.commit()

            return jsonify({'message': 'Message sent successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error sending message', 'error': str(e)}), 500

    # View sent messages
    # View sent messages
    @app.route('/sent_messages/<int:user_id>', methods=['GET'])
    def view_sent_messages(user_id):
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        try:
            messages = MessagesInbox.query.filter_by(sender_id=user_id).all()
            sent_messages = []

            for message in messages:
                recipient = User.query.get(message.user_id)
                sent_messages.append({
                    'id': message.id,
                    'recipient_id': message.user_id,
                    'recipient_name': recipient.username,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                    'message_type': "sent",
                    'is_read': message.is_read
                })

            return jsonify({'sent_messages': sent_messages}), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving sent messages', 'error': str(e)}), 500

    # View received messages
    @app.route('/received_messages/<int:user_id>', methods=['GET'])
    def view_received_messages(user_id):
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        try:
            messages = MessagesInbox.query.filter_by(user_id=user_id).all()
            received_messages = []

            for message in messages:
                sender = User.query.get(message.sender_id)
                received_messages.append({
                    'id': message.id,
                    'sender_id': message.sender_id,
                    'sender_name': sender.username,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                    'message_type': 'received',
                    'is_read': message.is_read
                })

            return jsonify({'received_messages': received_messages}), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving received messages', 'error': str(e)}), 500
