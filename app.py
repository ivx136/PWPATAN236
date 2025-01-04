from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import SessionLocal, User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = SessionLocal()
        user = db.query(User).filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            db.close()
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        db.close()
        flash('Invalid credentials!', 'danger')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']
        
        db = SessionLocal()
        if db.query(User).filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
            
        password_hash = generate_password_hash(password)
        new_user = User(username=username, role=role, email=email, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        db.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return render_template('dashboard.html', users=users)

@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']
        
        db = SessionLocal()
        password_hash = generate_password_hash(password)
        new_user = User(username=username, role=role, email=email, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        db.close()
        flash('User added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_user.html')

@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    db = SessionLocal()
    user = db.query(User).get(id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.role = request.form['role']
        user.email = request.form['email']
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'])
        db.commit()
        db.close()
        flash('User updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_user.html', user=user)

@app.route('/user/delete/<int:id>')
@login_required
def delete_user(id):
    db = SessionLocal()
    user = db.query(User).get(id)
    db.delete(user)
    db.commit()
    db.close()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)