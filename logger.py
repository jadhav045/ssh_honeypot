# logger.py
from datetime import datetime
import requests
import json

LOG_FILE = "logs/requests.log"
        
SESSION_FILE = "session/sessions.json"


# Add your ipstack API key here
IPSTACK_API_KEY = "88a5c21cee760c557b4a7059084adb5d"
IPSTACK_URL = f"http://api.ipstack.com/"

def geo_lookup(ip):
    # If the IP is localhost, return default values
    if ip == '127.0.0.1':
        return "Localhost", "Localhost"

    # Otherwise, perform the geo-location lookup
    response = requests.get(f"{IPSTACK_URL}{ip}?access_key={IPSTACK_API_KEY}")
    data = response.json()

    country = data.get('country_name', 'Unknown')
    city = data.get('city', 'Unknown')

    # Handle missing country/city data
    if country == "Unknown" or city == "Unknown":
        country = "Unidentified"
        city = "Unidentified"

    return country, city



def log_request(req):
    important_data = {
        'ip': req.remote_addr,
        'method': req.method,
        'user_agent': req.headers.get('User-Agent', 'N/A'),
    }

    # Get Geo-IP Lookup Data
    # country, city = geo_lookup(important_data['ip'])

    # with open(LOG_FILE, "a") as f:
    #     log_entry = f"[{datetime.now()}] IP: {important_data['ip']}, Method: {important_data['method']}, User-Agent: {important_data['user_agent']}, Country: {country}, City: {city}\n"
    #     f.write(log_entry)
    
    
     # If it's a POST request, capture the body (payload)
    payload_data = None
    if req.method == 'POST':
        if req.is_json:
            payload_data = req.get_json()  # For JSON bodies
        else:
            payload_data = req.form.to_dict()  # For form data
            
            
    with open(LOG_FILE, "a") as f:
        log_entry = f"[{datetime.now()}] IP: {important_data['ip']}, Method: {important_data['method']}, User-Agent: {important_data['user_agent']}"
        if payload_data:
            log_entry += f", Payload: {json.dumps(payload_data)}"  # Save the payload as JSON
        log_entry += "\n"
        f.write(log_entry)


def log_session_action(req):
    """
    Log the sequence of actions performed by the attacker (session replay).
    """
    session_data = {
        'ip': req.remote_addr,
        'action': req.path,  # Log the path visited
        'method': req.method,
        'user_agent': req.headers.get('User-Agent', 'N/A'),
        'timestamp': str(datetime.now())
    }

    # Save session data for replay
    with open(SESSION_FILE, "a") as f:
        f.write(json.dumps(session_data) + "\n")


def read_logs(filter_ip=None):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        if filter_ip:
            lines = [line for line in lines if filter_ip in line]
        return ''.join(lines)
    except FileNotFoundError:
        return "No logs found."
    

