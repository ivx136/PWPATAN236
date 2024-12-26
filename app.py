from flask import Flask, render_template, request, redirect, url_for
from models import SessionLocal, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        db = SessionLocal()
        new_user = User(username=username, role=role, email=email, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        db.close()

        return redirect(url_for('register'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)