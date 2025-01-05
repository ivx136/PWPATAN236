# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, UserForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    role=form.role.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Akun Anda telah dibuat! Anda dapat login sekarang.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Anda telah berhasil login!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login gagal. Periksa email dan password Anda.', 'danger')
    return render_template('login.html', form=form)

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('main.login'))
    users = User.query.all()
    return render_template('dashboard.html', users=users)

@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('main.login'))
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    role=form.role.data,
                    email=form.email.data)
        if form.password.data:
            user.set_password(form.password.data)
        else:
            flash('Password diperlukan untuk pengguna baru.', 'danger')
            return render_template('add_user.html', form=form)
        db.session.add(user)
        db.session.commit()
        flash('Pengguna baru telah ditambahkan!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_user.html', form=form)

@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('main.login'))
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        # Cek username dan email unik jika diubah
        if form.username.data != user.username:
            if User.query.filter_by(username=form.username.data).first():
                flash('Username sudah digunakan. Silakan pilih yang lain.', 'danger')
                return render_template('edit_user.html', form=form, user=user)
        if form.email.data != user.email:
            if User.query.filter_by(email=form.email.data).first():
                flash('Email sudah digunakan. Silakan pilih yang lain.', 'danger')
                return render_template('edit_user.html', form=form, user=user)
        user.username = form.username.data
        user.role = form.role.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Data pengguna telah diperbarui!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('edit_user.html', form=form, user=user)

@main.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('main.login'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Pengguna telah dihapus!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('main.login'))
