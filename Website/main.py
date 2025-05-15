from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from client import Client
from threading import Thread, Lock
import time

NAME_KEY = 'name'
client = None
messages = []

# Global dictionary to store Client objects
clients = {}

app = Flask(__name__)
app.secret_key = 'random string'

def disconnect():
    name = session.pop(NAME_KEY, None)
    if name in clients:
        del clients[name]


@app.route('/login', methods=['POST', 'GET'])
def login():
    disconnect()

    if request.method == 'POST':
        name = request.form['inputName']
        print(name)
        session[NAME_KEY] = name  # Store only the name in the session
        return redirect(url_for('home'))
    return render_template('login.html', **{"session": session})

@app.route('/logout')
def logout():
    name = session.pop(NAME_KEY, None)
    if name in clients:
        del clients[name]  # Remove the Client object when logging out
    return redirect(url_for('login'))

@app.route("/")
@app.route("/home")
def home():
    global client
    #don't let user access home page if not logged in
    if NAME_KEY not in session:
        return redirect(url_for('login'))
    
    name = session[NAME_KEY]
    if name not in clients:
        # Create a new Client object and store it in the global dictionary
        # name client object relationship in the global dictionary
        clients[name] = Client(name)

    client = clients[name]  # Assign the client to the global variable

    # Start the update_messages thread if not already started
    if not hasattr(client, "thread_started"):
        Thread(target=update_messages, daemon=True).start()
        client.thread_started = True

    print(f"Client initialized: {client.name}")
    print(f"Messages array: {messages}")

    return render_template("index.html", **{"login": True, "session": session})

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=['GET'])
def send_message():
    name = session.get(NAME_KEY)
    if not name or name not in clients:
        return "Client not found", 400

    client = clients[name]
    msg = request.args.get('val')
    if msg:
        print(f"Message from {name}: {msg}")
        client.send_message(msg)  # Add the message to the client's message list
        return "Message sent", 200
    return "No message provided", 400

@app.route("/get_messages", methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})

def update_messages():
    global messages  # Use the global `messages` list
    while True:
        time.sleep(0.1)
        if client:  # Ensure `client` is initialized
            try:
                new_messages = client.get_messages()  # Fetch new messages from the client
                if new_messages:
                    print(f"New messages: {new_messages}")  # Debug: Print new messages
                    messages.extend(new_messages)  # Add new messages to the global `messages` list
                    print(f"Updated messages array: {messages}")  # Debug: Print the updated messages array
            except Exception as e:
                print(f"Error in update_messages: {e}")

if __name__ == '__main__':
    # Thread(target=update_messages).start()
    app.run(debug=True)