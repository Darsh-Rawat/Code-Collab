import os
import json
import uuid
import logging
import subprocess
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-development")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after app initialization
from models import User, Room, Message, CodeSnippet

# In-memory storage for our data
users = {}
rooms = {}
user_rooms = {}
messages = {}
code_snippets = {}

# Load existing data if available
def load_data():
    global users, rooms, user_rooms, messages, code_snippets
    try:
        if os.path.exists('data/users.json'):
            with open('data/users.json', 'r') as f:
                users = json.load(f)
        if os.path.exists('data/rooms.json'):
            with open('data/rooms.json', 'r') as f:
                rooms = json.load(f)
        if os.path.exists('data/user_rooms.json'):
            with open('data/user_rooms.json', 'r') as f:
                user_rooms = json.load(f)
        if os.path.exists('data/messages.json'):
            with open('data/messages.json', 'r') as f:
                messages = json.load(f)
        if os.path.exists('data/code_snippets.json'):
            with open('data/code_snippets.json', 'r') as f:
                code_snippets = json.load(f)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        # Ensure we have the data directory
        os.makedirs('data', exist_ok=True)

# Save data to disk
def save_data():
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/users.json', 'w') as f:
            json.dump(users, f)
        with open('data/rooms.json', 'w') as f:
            json.dump(rooms, f)
        with open('data/user_rooms.json', 'w') as f:
            json.dump(user_rooms, f)
        with open('data/messages.json', 'w') as f:
            json.dump(messages, f)
        with open('data/code_snippets.json', 'w') as f:
            json.dump(code_snippets, f)
    except Exception as e:
        logging.error(f"Error saving data: {e}")

# Load data at startup
load_data()

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user_data = users[user_id]
        user = User(
            id=user_id,
            username=user_data['username'],
            email=user_data['email'],
            country=user_data['country']
        )
        user.set_password_hash(user_data['password_hash'])
        return user
    return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user_id = None
        for uid, user_data in users.items():
            if user_data['email'] == email:
                user_id = uid
                break
        
        if user_id:
            user_data = users[user_id]
            if check_password_hash(user_data['password_hash'], password):
                user = User(
                    id=user_id,
                    username=user_data['username'],
                    email=user_data['email'],
                    country=user_data['country']
                )
                user.set_password_hash(user_data['password_hash'])
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('User not found', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        country = request.form.get('country')
        
        # Check if username or email already exists
        for user_data in users.values():
            if user_data['username'] == username:
                flash('Username already exists', 'danger')
                return render_template('register.html')
            if user_data['email'] == email:
                flash('Email already exists', 'danger')
                return render_template('register.html')
        
        # Create new user
        user_id = str(uuid.uuid4())
        users[user_id] = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'country': country,
            'created_at': datetime.now().isoformat()
        }
        
        # Initialize user_rooms for this user
        user_rooms[user_id] = []
        
        # Save data
        save_data()
        
        # Create user instance and login
        user = User(
            id=user_id,
            username=username,
            email=email,
            country=country
        )
        user.set_password_hash(users[user_id]['password_hash'])
        login_user(user)
        
        flash('Registration successful!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get rooms for the current user
    user_room_ids = user_rooms.get(current_user.id, [])
    user_room_data = []
    
    for room_id in user_room_ids:
        if room_id in rooms:
            room_data = rooms[room_id]
            user_room_data.append({
                'id': room_id,
                'name': room_data['name'],
                'created_at': room_data['created_at'],
                'has_password': bool(room_data.get('password_hash'))
            })
    
    return render_template('dashboard.html', rooms=user_room_data)

@app.route('/create_room', methods=['POST'])
@login_required
def create_room():
    room_name = request.form.get('room_name')
    password = request.form.get('password')
    
    # Create new room
    room_id = str(uuid.uuid4())
    rooms[room_id] = {
        'name': room_name,
        'owner_id': current_user.id,
        'password_hash': generate_password_hash(password) if password else None,
        'created_at': datetime.now().isoformat(),
        'active_users': []
    }
    
    # Add room to user's rooms
    if current_user.id not in user_rooms:
        user_rooms[current_user.id] = []
    user_rooms[current_user.id].append(room_id)
    
    # Initialize messages for this room
    messages[room_id] = []
    
    # Initialize code snippet for this room
    code_snippets[room_id] = {
        'code': '// Write your code here',
        'language': 'javascript',
        'last_updated_by': current_user.id,
        'last_updated_at': datetime.now().isoformat()
    }
    
    # Save data
    save_data()
    
    flash('Room created successfully!', 'success')
    return redirect(url_for('room', room_id=room_id))

@app.route('/join_room', methods=['POST'])
@login_required
def join_room_route():
    room_id = request.form.get('room_id')
    password = request.form.get('password', '')
    
    if room_id not in rooms:
        flash('Room not found', 'danger')
        return redirect(url_for('dashboard'))
    
    room_data = rooms[room_id]
    
    # Check if password is required and correct
    if room_data.get('password_hash') and not check_password_hash(room_data['password_hash'], password):
        flash('Invalid password', 'danger')
        return redirect(url_for('dashboard'))
    
    # Add room to user's rooms if not already there
    if current_user.id not in user_rooms:
        user_rooms[current_user.id] = []
    if room_id not in user_rooms[current_user.id]:
        user_rooms[current_user.id].append(room_id)
        save_data()
    
    return redirect(url_for('room', room_id=room_id))

@app.route('/room/<room_id>')
@login_required
def room(room_id):
    # Check if room exists
    if room_id not in rooms:
        flash('Room not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if user has access to this room
    if current_user.id not in user_rooms or room_id not in user_rooms[current_user.id]:
        flash('You do not have access to this room', 'danger')
        return redirect(url_for('dashboard'))
    
    room_data = rooms[room_id]
    room_messages = messages.get(room_id, [])
    code_snippet = code_snippets.get(room_id, {
        'code': '// Write your code here',
        'language': 'javascript'
    })
    
    return render_template(
        'room.html',
        room=room_data,
        room_id=room_id,
        messages=room_messages,
        code=code_snippet['code'],
        language=code_snippet['language']
    )

@app.route('/execute_code', methods=['POST'])
@login_required
def execute_code():
    data = request.json
    room_id = data.get('room_id')
    code = data.get('code')
    language = data.get('language', 'javascript')
    
    # Validate room and access
    if room_id not in rooms or current_user.id not in user_rooms or room_id not in user_rooms[current_user.id]:
        return jsonify({'error': 'Access denied or room not found'}), 403
    
    result = ""
    error = ""
    
    try:
        if language == 'javascript':
            with tempfile.NamedTemporaryFile(suffix='.js', delete=False) as temp:
                temp.write(code.encode())
                temp_name = temp.name
            
            proc = subprocess.run(['node', temp_name], capture_output=True, text=True, timeout=10)
            os.unlink(temp_name)
            
            if proc.returncode == 0:
                result = proc.stdout
            else:
                error = proc.stderr
        
        elif language == 'python':
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
                temp.write(code.encode())
                temp_name = temp.name
            
            proc = subprocess.run(['python', temp_name], capture_output=True, text=True, timeout=10)
            os.unlink(temp_name)
            
            if proc.returncode == 0:
                result = proc.stdout
            else:
                error = proc.stderr
        
        else:
            error = f"Language {language} not supported"
    
    except subprocess.TimeoutExpired:
        error = "Execution timed out (10s limit)"
    except Exception as e:
        error = f"Execution error: {str(e)}"
    
    return jsonify({
        'result': result,
        'error': error
    })

@app.route('/download_code', methods=['POST'])
@login_required
def download_code():
    data = request.json
    room_id = data.get('room_id')
    language = data.get('language', 'javascript')
    
    # Validate room and access
    if room_id not in rooms or current_user.id not in user_rooms or room_id not in user_rooms[current_user.id]:
        return jsonify({'error': 'Access denied or room not found'}), 403
    
    code_snippet = code_snippets.get(room_id, {'code': '// Empty code', 'language': language})
    code = code_snippet['code']
    
    file_extension = '.js' if language == 'javascript' else '.py' if language == 'python' else '.txt'
    filename = f"code{file_extension}"
    
    return jsonify({
        'code': code,
        'filename': filename
    })

# Socket.IO events
@socketio.on('connect')
def handle_connect():
    logging.debug(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    logging.debug(f"Client disconnected: {request.sid}")

@socketio.on('join')
def handle_join(data):
    room_id = data.get('room_id')
    
    # Validate room and access
    if not current_user.is_authenticated or room_id not in rooms:
        return
    
    if current_user.id not in user_rooms or room_id not in user_rooms[current_user.id]:
        return
    
    join_room(room_id)
    
    # Add user to active users
    if current_user.id not in rooms[room_id]['active_users']:
        rooms[room_id]['active_users'].append(current_user.id)
    
    # Notify room about new user
    emit('user_joined', {
        'username': current_user.username,
        'user_id': current_user.id,
        'active_users': [users[uid]['username'] for uid in rooms[room_id]['active_users'] if uid in users]
    }, room=room_id)
    
    # Send current code state to the joining user
    emit('code_updated', {
        'code': code_snippets.get(room_id, {}).get('code', '// Write your code here'),
        'language': code_snippets.get(room_id, {}).get('language', 'javascript'),
        'updated_by': users.get(code_snippets.get(room_id, {}).get('last_updated_by'), {}).get('username', 'Unknown')
    })
    
    # Send recent messages
    room_messages = messages.get(room_id, [])[-50:]  # Last 50 messages
    emit('load_messages', {'messages': room_messages})

@socketio.on('leave')
def handle_leave(data):
    room_id = data.get('room_id')
    
    # Validate room
    if not current_user.is_authenticated or room_id not in rooms:
        return
    
    leave_room(room_id)
    
    # Remove user from active users
    if current_user.id in rooms[room_id]['active_users']:
        rooms[room_id]['active_users'].remove(current_user.id)
    
    # Notify room about user leaving
    emit('user_left', {
        'username': current_user.username,
        'user_id': current_user.id,
        'active_users': [users[uid]['username'] for uid in rooms[room_id]['active_users'] if uid in users]
    }, room=room_id)

@socketio.on('send_message')
def handle_message(data):
    room_id = data.get('room_id')
    message_content = data.get('message')
    
    # Validate room and access
    if not current_user.is_authenticated or room_id not in rooms:
        return
    
    if current_user.id not in user_rooms or room_id not in user_rooms[current_user.id]:
        return
    
    # Create and store message
    message = {
        'id': str(uuid.uuid4()),
        'user_id': current_user.id,
        'username': current_user.username,
        'content': message_content,
        'timestamp': datetime.now().isoformat()
    }
    
    if room_id not in messages:
        messages[room_id] = []
    
    messages[room_id].append(message)
    save_data()
    
    # Send message to room
    emit('new_message', message, room=room_id)

@socketio.on('update_code')
def handle_code_update(data):
    room_id = data.get('room_id')
    code = data.get('code')
    language = data.get('language', 'javascript')
    
    # Validate room and access
    if not current_user.is_authenticated or room_id not in rooms:
        return
    
    if current_user.id not in user_rooms or room_id not in user_rooms[current_user.id]:
        return
    
    # Update code snippet
    if room_id not in code_snippets:
        code_snippets[room_id] = {}
    
    code_snippets[room_id] = {
        'code': code,
        'language': language,
        'last_updated_by': current_user.id,
        'last_updated_at': datetime.now().isoformat()
    }
    
    save_data()
    
    # Broadcast code update to room
    emit('code_updated', {
        'code': code,
        'language': language,
        'updated_by': current_user.username
    }, room=room_id, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
