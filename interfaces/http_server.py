# interfaces/http_server.py
from flask import Flask, request, render_template_string
from logger import log_request, read_logs, log_session_action

app = Flask(__name__)

# Fake Admin Page
@app.route('/admin', methods=['GET'])
def fake_admin():
    # Display a fake admin dashboard with decoy data
    return """
    <h2>Fake Admin Dashboard</h2>
    <p>Welcome to the fake admin interface. No real data is here.</p>
    <ul>
        <li>User: JohnDoe | Role: Admin</li>
        <li>User: JaneSmith | Role: User</li>
    </ul>
    """

@app.route('/', methods=['GET', 'POST'])
def fake_login():
    log_request(request)
    return """
    <h2>Fake Login Page</h2>
    <form action="/login" method="post">
        Username: <input type='text' name='username'><br>
        Password: <input type='password' name='password'><br>
        <input type='submit' value='Login'>
    </form>
    """

# Login Handler
@app.route('/login', methods=['POST'])
def handle_login():
    log_request(request)
    log_session_action(request)  # Track the action for session replay
    # log_payload(request)  # Save the POST body (username/password)

    username = request.form.get('username')
    password = request.form.get('password')

    # Simulate login logic
    if username == "admin":
        return "Welcome admin, you have full access!"
    elif username == "guest":
        return "Welcome guest, limited access granted."
    else:
        return "Invalid credentials. Please try again."

@app.route('/logs')
def view_logs():
    filter_ip = request.args.get('ip')
    logs = read_logs(filter_ip)
    return render_template_string("""
    <h2>Log Viewer</h2>
    <form method="get">
        Filter by IP: <input name="ip" value="{{ filter_ip }}">
        <input type="submit" value="Filter">
    </form>
    <pre>{{ logs }}</pre>
    """, logs=logs, filter_ip=filter_ip or "")

def start_http():
    app.run(host='0.0.0.0', port=8080)

