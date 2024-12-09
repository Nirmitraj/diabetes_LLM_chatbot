from flask import Blueprint, request, jsonify, render_template, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models import User, LoginHistory, ChatHistory
from app.llm import get_user_query_response
from datetime import datetime
from flask import session
from flask import redirect, url_for



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html') 

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  # Render the registration form

    # Process POST request for registration
    data = request.get_json()
    if not data or not all(key in data for key in ['email', 'password', 'full_name']):
        return jsonify({'message': 'Missing data in registration request!'}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists!'}), 400

    # Hash the password and save the new user
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password, full_name=data['full_name'])
    db.session.add(new_user)
    db.session.commit()

    # Log in the new user automatically by setting up the session
    session['user_name'] = new_user.full_name
    session['user_email'] = new_user.email
    session['chat_history'] = []

    return jsonify({'message': 'User registered successfully!', 'redirect_url': url_for('main.main_page')})



from flask import session

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json()
    user = User.query.filter_by(email=data['email'], is_active=1).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Set up session variables
        session['chat_history'] = []
        session['user_name'] = user.full_name  # Store the user's name in session
        session['user_email'] = user.email  # Store the user's email in session

        # Create access token
        access_token = create_access_token(identity={'id': user.id, 'email': user.email})

        # Store JWT token in session
        session['access_token'] = access_token

        # Record login history
        login_history = LoginHistory(user_id=user.id, timestamp=datetime.utcnow())
        db.session.add(login_history)
        db.session.commit()

        # Log the session data for debugging
        print("Session data after login:", session)

        # Return the token and redirect URL
        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'redirect_url': url_for('main.main_page')
        })
    else:
        return jsonify({'message': 'Login failed!'}), 401


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


@main.route('/main')
def main_page():
    user_name = session.get('user_name', 'Guest')
    user_email = session.get('user_email', 'guest@example.com')
    return render_template('main.html', user_name=user_name, user_email=user_email)


@main.route('/getting-started')
def getting_started():
    return render_template('getting-started.html')

@main.route('/user-profile')
def user_profile():
    user_name = session.get('user_name', 'Guest')
    user_email = session.get('user_email', 'guest@example.com')
    print("User email from session:", user_email)  # Debugging line
    return render_template('user-profile.html', user_name=user_name, user_email=user_email)

@main.route('/user-activities')
def user_activities():
    user_name = session.get('user_name', 'Guest')
    user_email = session.get('user_email', 'guest@example.com')
    return render_template('user-activities.html',user_name=user_name, user_email=user_email)

@main.route('/user-profile-settings')
def user_profile_settings():
    user_name = session.get('user_name', 'Guest')
    user_email = session.get('user_email', 'guest@example.com')
    return render_template('user-profile-settings.html',user_name=user_name, user_email=user_email)

@main.route('/user-account-settings')
def user_account_settings():
    user_name = session.get('user_name', 'Guest')
    user_email = session.get('user_email', 'guest@example.com')
    return render_template('user-account-settings.html',user_name=user_name, user_email=user_email)


@main.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.filter_by(is_active=1).all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'age': user.age,
            'gender': user.gender,
            'street_address': user.street_address,
            'city': user.city,
            'state': user.state,
            'country': user.country,
            'zip': user.zip,
            'diagnose_date': user.diagnose_date,
            'blood_glucose_level': user.blood_glucose_level,
            'blood_glucose_fasting_level': user.blood_glucose_fasting_level,
            'medications': user.medications,
            'medical_conditions': user.medical_conditions,
            'dietary_pref': user.dietary_pref,
            'physical_activity': user.physical_activity,
            'weight': user.weight,
            'height': user.height,
            'management_goals': user.management_goals,
            'learning_preference': user.learning_preference,
            'created_on': user.created_on
        }
        output.append(user_data)
    return jsonify({'users': output})

@main.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.filter_by(id=user_id, is_active=1).first() 
    if not user:
        return jsonify({'message': 'User not found!'})
    user_data = {
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'age': user.age,
        'gender': user.gender,
        'street_address': user.street_address,
        'city': user.city,
        'state': user.state,
        'country': user.country,
        'zip': user.zip,
        'diagnose_date': user.diagnose_date,
        'blood_glucose_level': user.blood_glucose_level,
        'blood_glucose_fasting_level': user.blood_glucose_fasting_level,
        'medications': user.medications,
        'medical_conditions': user.medical_conditions,
        'dietary_pref': user.dietary_pref,
        'physical_activity': user.physical_activity,
        'weight': user.weight,
        'height': user.height,
        'management_goals': user.management_goals,
        'learning_preference': user.learning_preference,
        'created_on': user.created_on
    }
    return jsonify({'user': user_data})

@main.route('/user/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id, is_active=1).first()
    if not user:
        return jsonify({'message': 'User not found!'})
    user.email = data.get('email', user.email)
    user.full_name = data.get('full_name', user.full_name)
    user.age = data.get('age', user.age)
    user.gender = data.get('gender', user.gender)
    user.street_address = data.get('street_address', user.street_address)
    user.city = data.get('city', user.city)
    user.state = data.get('state', user.state)
    user.country = data.get('country', user.country)
    user.zip = data.get('zip', user.zip)
    user.blood_glucose_level = data.get('blood_glucose_level', user.blood_glucose_level)
    user.blood_glucose_fasting_level = data.get('blood_glucose_fasting_level', user.blood_glucose_fasting_level)
    user.medications = data.get('medications', user.medications)
    user.medical_conditions = data.get('medical_conditions', user.medical_conditions)
    user.dietary_pref = data.get('dietary_pref', user.dietary_pref)
    user.physical_activity = data.get('physical_activity', user.physical_activity)
    user.weight = data.get('weight', user.weight)
    user.height = data.get('height', user.height)
    user.management_goals = data.get('management_goals', user.management_goals)
    user.learning_preference = data.get('learning_preference', user.learning_preference)
    
    if 'diagnose_date' in data:
        user.diagnose_date = datetime.strptime(data.get('diagnose_date') , "%Y-%m-%d")
    else:
        user.diagnose_date

    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})

@main.route('/user/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.filter_by(id=user_id, is_active=1).first()
    if not user:
        return jsonify({'message': 'User not found!'})
    user.is_active = 0
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})

@main.route('/chat', methods=['GET', 'POST'])
@jwt_required(optional=True)
def chat():
    if request.method == 'GET':
        current_app.logger.info("GET /chat request received.")
        return render_template('chat.html')

    # Process the POST request to handle chat actions
    data = request.get_json()
    current_app.logger.info("POST /chat request received with data: %s", data)
    current_app.logger.info("Session Data: %s", dict(session))

    if not data:
        current_app.logger.warning("Invalid request: Missing data.")
        return jsonify({'message': 'Invalid request: missing data'}), 400

    current_user = get_jwt_identity()
    user_id = current_user.get('id') if current_user else None
    current_chat_id = session.get('current_chat_id', None)  # Track active chat session

    # Handle "new-chat" event
    if data.get('new_chat', False):
        current_app.logger.info("Frontend requested a new chat.")

        # Collect the messages from the current conversation
        messages = data.get('messages', [])
        chat_content = "\n".join(
            [f"{'User' if msg['isUser'] else 'Assistant'}: {msg['content']}" for msg in messages]
        )

        if user_id:
            # Create a new chat row in the database with the collected messages
            new_chat = ChatHistory(
                user_id=user_id,
                title=f"Chat {user_id} {datetime.utcnow()}",
                last_message=messages[-1]['content'] if messages else "",
                role='user',
                content=chat_content,  # Add all current messages
                timestamp=datetime.utcnow(),
            )
            db.session.add(new_chat)
            db.session.commit()

            # Update session to track new chat
            current_chat_id = new_chat.id
            session['current_chat_id'] = current_chat_id

            current_app.logger.info(
                "New chat created with ID: %s and content:\n%s", current_chat_id, chat_content
            )
        return jsonify({'message': 'New chat created'}), 201

    # Handle a user query
    if 'query' in data:
        user_query = data['query']
        current_app.logger.info("Processing user query: %s", user_query)

        # Append the user's query to the current chat
        if user_id and current_chat_id:
            chat_history_entry = ChatHistory.query.filter_by(id=current_chat_id).first()
            if chat_history_entry:
                chat_history_entry.content += f"\nUser: {user_query}"
                chat_history_entry.last_message = user_query
                db.session.commit()
                current_app.logger.info("User query added to chat ID %s", current_chat_id)
            else:
                current_app.logger.warning("No active chat found for ID %s", current_chat_id)

        # Generate the AI response
        chat_history = session.get('chat_history', [])
        chat_history.append({'role': 'user', 'content': user_query})

        response = get_user_query_response(user_query, chat_history)
        if response:
            # Append AI response to the chat
            if user_id and current_chat_id:
                if chat_history_entry:
                    chat_history_entry.content += f"\nAssistant: {response}"
                    chat_history_entry.last_message = response
                    db.session.commit()
                    current_app.logger.info("AI response added to chat ID %s", current_chat_id)

            # Update session chat history
            chat_history.append({'role': 'assistant', 'content': response})
            session['chat_history'] = chat_history

            current_app.logger.info("Chat response sent back to user.")
            return jsonify({'response': response})
        else:
            current_app.logger.error("Failed to generate AI response.")
            return jsonify({'message': 'Request could not be processed.'}), 500

    # Handle invalid cases
    current_app.logger.warning("Invalid request: Missing 'query' or 'new_chat'.")
    return jsonify({'message': 'Invalid request: missing query or new_chat'}), 400

@main.route('/get-chat-history', methods=['GET'])
@jwt_required()
def getChatHistory():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'message': 'User not authenticated'}), 401

        user_id = current_user.get('id')
        if not user_id:
            return jsonify({'message': 'Invalid user'}), 401

        # Fetch chat history for the user
        chat_history_records = ChatHistory.query.filter_by(user_id=user_id).all()

        # Prepare the chat history data
        chat_history = []
        for record in chat_history_records:
            messages = [
                {'content': line.split(": ", 1)[1], 'isUser': line.startswith("User")}
                for line in record.content.split("\n")
                if ": " in line
            ]
            chat_history.append({
                'id': record.id,
                'title': record.title,
                'messages': messages,
                'timestamp': record.timestamp
            })

        return jsonify({'chat_history': chat_history}), 200