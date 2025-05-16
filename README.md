# Real-Time Chat Application

A real-time chat application built with Python Flask, Socket Programming, and a clean Bootstrap UI.

## Features

- Real-time messaging using WebSocket-like connections
- User authentication and session management
- Clean and responsive Bootstrap UI
- Multi-threaded server to handle multiple client connections
- Browser-based chat interface

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, JavaScript, jQuery
- **Styling**: Bootstrap 5
- **Networking**: Python Socket Programming
- **Template Engine**: Jinja2

## Project Structure

```
├── server/
│   └── server.py         # Socket server implementation
├── Website/
│   ├── client/          
│   │   └── client.py     # Client socket handler
│   ├── static/
│   │   └── index.js      # Frontend JavaScript
│   ├── templates/        # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── login.html
│   └── main.py          # Flask application
```

## Setup and Installation

1. Clone the repository
```bash
git clone <repository-url>
```

2. Install dependencies
```bash
pip install flask
```

3. Start the server
```bash
python server/server.py
```

4. Run the Flask application
```bash
python Website/main.py
```

5. Access the application at `http://localhost:5000`

## Work in Progress

This project is currently under development. Planned features include:
- Persistent message storage
- Private messaging
- User profiles
- Message encryption

## Contributing

Feel free to fork the project and submit pull requests for any improvements.
