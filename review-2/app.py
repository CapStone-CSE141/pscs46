import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, join_room, leave_room, emit
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') 

socketio = SocketIO(app)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'email' in session:
        print("Email found in session")
        return redirect(url_for('dashboard')) 
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        print('No email found in session')
        return redirect(url_for('index')) 
    print('Session Data: ', session)
    return render_template('dashboard.html', email=session['email'])

@app.route('/research', methods=['GET', 'POST'])
def research():
    if 'email' in session:
        print("Email found in session")
        return render_template('user_research.html', email=session['email'])
    print("No session found")
    return render_template('research.html') 

@app.route('/user_research', methods=['GET', 'POST'])
def user_research():
    if 'email' not in session:
        print('No email found in session')
        return redirect(url_for('research')) 
    print('Session Data: ', session)
    return render_template('user_research.html', email=session['email'])

@app.route('/telemedicine', methods=['GET', 'POST'])
def telemedicine():
    if 'email' in session:
        print("Email found in session")
        return render_template('user_telemedicine.html', email=session['email'])
    return render_template('telemedicine.html')

@app.route('/user_telemedicine', methods=['GET', 'POST'])
def user_telemedicine():
    if 'email' not in session:
        print("No Email found in session")
        return redirect(url_for('telemedicine')) 
    return render_template('user_telemedicine.html', email=session['email'])

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    if 'email' in session:
        print("Email found in session")
        return render_template('user_ai.html', email=session['email'])
    return render_template('ai.html')

@app.route('/user_ai', methods=['GET', 'POST'])
def user_ai():
    if 'email' not in session:
        print("Email not found in session")
        return render_template('ai.html')  
    return render_template('user_ai.html', email=session['email'])

@app.route('/chat_interface',methods=['GET','POST'])
def chat_interface():
    if 'email' not in session:
        return render_template('index.html')
    
    return render_template('chat_interface.html',email=session['email'])

@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    if 'email' in session:
        print("Email found in session")
        return render_template('user_aboutus.html', email=session['email'])
    return render_template('aboutus.html')

@app.route('/user_aboutus', methods=['GET', 'POST'])
def user_aboutus():
    if 'email' not in session:
        print("Email not found in session")
        return render_template('aboutus.html')  
    return render_template('user_aboutus.html', email=session['email'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return 'Passwords do not match'
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['email'] = user[2]
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid Email or Password'

    return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/video_call/', methods=['GET'])
def video_call(room):
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('video_call.html', room=room, email=session['email'])

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('user_joined', {'email': session['email']}, room=room)

@socketio.on('signal')
def on_signal(data):
    room = data['room']
    emit('signal', data, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
