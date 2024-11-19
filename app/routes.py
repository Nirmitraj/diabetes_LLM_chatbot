from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models import User, LoginHistory
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
        session['chat_history'] = []
        session['user_name'] = user.full_name  # Store the user's name in session
        session['user_email'] = user.email  # Store the user's email in session

        print("Session data after login:", session)

        # Create access token and record login history
        access_token = create_access_token(identity={'id': user.id, 'email': user.email})
        login_history = LoginHistory(user_id=user.id, timestamp=datetime.utcnow())
        db.session.add(login_history)
        db.session.commit()
        
        return jsonify({'access_token': access_token, 'user_id': user.id, 'redirect_url': url_for('main.main_page')})
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

@main.route('/chat', methods=['GET', 'POST'])
@jwt_required(optional=True)  # Only require JWT for POST
def chat():
    user_id = None
    if get_jwt_identity():  # Check if a valid JWT exists
        current_user = get_jwt_identity()
        user_id = current_user['id']

    if request.method == 'GET':
        # Fetch chat history for the current user if authenticated
        if user_id:
            user_chats = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.timestamp).all()
            chat_history = [{'role': chat.role, 'content': chat.content, 'timestamp': chat.timestamp} for chat in user_chats]
        else:
            chat_history = []
        return jsonify({'chat_history': chat_history})
    
    # Handle POST request
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'message': 'Invalid request: missing query'}), 400

    # Generate the response
    chat_history = session.get('chat_history', [])
    chat_history.append({'role': 'user', 'content': data['query']})
    response = get_user_query_response(data['query'], chat_history)

    if response:
        if user_id:
            # Fetch or create a new ChatHistory entry
            chat_title = data.get('title', 'Untitled Chat')  # Optional chat title from the request
            existing_chat = ChatHistory.query.filter_by(user_id=user_id, title=chat_title).first()

            if existing_chat:
                # Update the existing chat's last message and timestamp
                existing_chat.last_message = response
                existing_chat.timestamp = datetime.utcnow()
                db.session.commit()
                chat_id = existing_chat.id
            else:
                # Create a new chat entry
                new_chat = ChatHistory(
                    user_id=user_id,
                    title=chat_title,
                    last_message=response,
                    timestamp=datetime.utcnow(),
                    role='assistant',
                    content=response
                )
                db.session.add(new_chat)
                db.session.commit()
                chat_id = new_chat.id

            # Save user query and assistant response to the database
            user_message = ChatHistory(user_id=user_id, role='user', content=data['query'], title=chat_title)
            assistant_message = ChatHistory(user_id=user_id, role='assistant', content=response, title=chat_title)
            db.session.add_all([user_message, assistant_message])
            db.session.commit()

        # Add to session chat history
        chat_history.append({'role': 'assistant', 'content': response})
        session['chat_history'] = chat_history

        # Include chat_id and last_message in the response
        return jsonify({
            'response': response,
            'chat_id': chat_id,
            'last_message': response,
        })

    else:
        return jsonify({'message': 'Request could not be processed.'}), 500

        
@main.route('/chat/history', methods=['GET'])
@jwt_required(optional=True)  # Only require JWT for logged-in users
def get_chat_history():
    current_user_id = None
    if get_jwt_identity():  # Check if a valid JWT exists
        current_user = get_jwt_identity()
        current_user_id = current_user['id']

    if not current_user_id:
        return jsonify({'message': 'User not authenticated.'}), 403

    # Fetch chat summaries (titles, last messages) for the current user
    chat_summaries = (
        db.session.query(
            ChatHistory.title, 
            ChatHistory.last_message, 
            ChatHistory.timestamp
        )
        .filter_by(user_id=current_user_id)
        .order_by(ChatHistory.timestamp.desc())
        .all()
    )

    # Format data for frontend
    response_data = [
        {
            'title': chat.title,
            'last_message': chat.last_message,
            'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for chat in chat_summaries
    ]

    return jsonify(response_data)        
    
@main.route('/update-chat/<int:chat_id>', methods=['PUT'])
@jwt_required()
def update_chat(chat_id):
    data = request.get_json()
    if not data or 'last_message' not in data:
        return jsonify({'message': 'Invalid request: missing required fields'}), 400

    # Fetch the chat by its ID
    chat = ChatHistory.query.filter_by(id=chat_id).first()
    if not chat:
        return jsonify({'message': 'Chat not found'}), 404

    # Update the last message and any other fields
    chat.last_message = data['last_message']
    db.session.commit()

    return jsonify({'message': 'Chat updated successfully!'})    