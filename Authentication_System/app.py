from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Needed to give out "Session Cookies"
app.config["JWT_SECRET_KEY"] = "super-secret-jwt-key"
jwt = JWTManager(app)

# 1. Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='52775336185-f488rr9gnjqdatt4nbt5u7d13ntshcmi.apps.googleusercontent.com',
    client_secret='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',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Mock User Data 
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.route('/')
def home():
    # If already logged in, go straight to dashboard
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # 1. Check for JSON data (Postman)
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    # 2. Fallback to Form data (HTML Page)
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    # 3. Validation Logic
    if username == "admin" and password == "password123":
        # Handle success based on request type
        if request.is_json:
            access_token = create_access_token(identity=username)
            return {"access_token": access_token}, 200
        else:
            session['user'] = username
            return redirect(url_for('dashboard'))
            
    # 4. Handle Failure
    if request.is_json:
        return {"msg": "Invalid Credentials!"}, 401
    else:
        return render_template('login.html', error="Invalid Credentials!")

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# 2. The Login Trigger
@app.route('/login/google')
def google_login():
    # Redirect to Google's login page
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri, access_type='offline', prompt='consent')

# 3. The Callback (The "Authorize" route you put in Google Console)
@app.route('/authorize')
def authorize():
    # Trade the code from Google for a user token
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        session['user'] = user_info['email']
        # You could also generate a JWT here if you wanted a hybrid system
        return redirect(url_for('dashboard'))
    
    return "Google login failed", 400

@app.route('/dashboard')
def dashboard():
    # Security Check: 
    if 'user' in session:
        return f"<h1>Welcome, {session['user']}!</h1> <a href='/logout'>Logout</a>"
    
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None) 
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)