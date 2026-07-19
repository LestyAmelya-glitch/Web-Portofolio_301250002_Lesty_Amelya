from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Project, Message, Profile, Skill
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'Lesty')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'Lestya008')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fc60cf590cd02135807bedfca6aabb00')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db.init_app(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    profile = Profile.query.first()
    return render_template('index.html', profile=profile)

@app.route('/about')
def about():
    profile = Profile.query.first()
    skills = Skill.query.all()
    return render_template('about.html', profile=profile, skills=skills)

@app.route('/portofolio')
def portofolio():
    projects = Project.query.all()
    return render_template('portofolio.html', projects=projects)

@app.route('/portofolio/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)

@app.route('/kontak', methods=['GET', 'POST'])
def kontak():
    profile = Profile.query.first()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for('kontak'))

    return render_template('kontak.html', profile=profile)

@app.route('/dashboard/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['user'] = username
            return redirect(url_for('dashboard_index'))
        else:
            return render_template('dashboard/login.html', error='Username atau password salah!')

    return render_template('dashboard/login.html')

@app.route('/dashboard')
def dashboard_index():
    if 'user' not in session:
        return redirect(url_for('login'))

    total_projects = Project.query.count()
    unread_messages = Message.query.filter_by(is_read=False).count()

    return render_template('dashboard/index.html', total_projects=total_projects, unread_messages=unread_messages)

@app.route('/dashboard/projects')
def dashboard_projects():
    if 'user' not in session:
        return redirect(url_for('login'))

    projects = Project.query.all()
    return render_template('dashboard/projects.html', projects=projects)

@app.route('/dashboard/projects/add', methods=['GET', 'POST'])
def add_project():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        technologies = request.form.get('technologies')
        github_link = request.form.get('github_link')
        live_link = request.form.get('live_link')
        file = request.files.get('image')

        image_filename = 'default.jpg'
        if file and file.filename != '' and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        new_project = Project(
            title=title,
            description=description,
            technologies=technologies,
            image_file=image_filename,
            github_link=github_link,
            live_link=live_link
        )
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('dashboard_projects'))

    return render_template('dashboard/add_project.html')

@app.route('/dashboard/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.technologies = request.form.get('technologies')
        project.github_link = request.form.get('github_link')
        project.live_link = request.form.get('live_link')

        file = request.files.get('image')
        if file and file.filename != '' and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            project.image_file = image_filename

        db.session.commit()
        return redirect(url_for('dashboard_projects'))

    return render_template('dashboard/edit_project.html', project=project)

@app.route('/dashboard/projects/delete/<int:id>', methods=['POST'])
def delete_project(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('dashboard_projects'))

@app.route('/dashboard/messages')
def dashboard_messages():
    if 'user' not in session:
        return redirect(url_for('login'))

    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('dashboard/messages.html', messages=messages)

@app.route('/dashboard/messages/read/<int:id>', methods=['POST'])
def mark_read(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    message = Message.query.get_or_404(id)
    message.is_read = True
    db.session.commit()

    return redirect(url_for('dashboard_messages'))

@app.route('/dashboard/messages/delete/<int:id>', methods=['POST'])
def delete_message(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()

    return redirect(url_for('dashboard_messages'))

@app.route('/dashboard/profile', methods=['GET', 'POST'])
def dashboard_profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    profile = Profile.query.first()
    skills = Skill.query.all()

    if request.method == 'POST':
        profile.name = request.form.get('name')
        profile.headline = request.form.get('headline')
        profile.about = request.form.get('about')
        profile.email = request.form.get('email')
        profile.github = request.form.get('github')
        profile.linkedin = request.form.get('linkedin')

        file = request.files.get('photo')
        if file and file.filename != '' and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            profile.photo = image_filename

        db.session.commit()
        return redirect(url_for('dashboard_profile'))

    return render_template('dashboard/profile.html', profile=profile, skills=skills)

@app.route('/dashboard/profile/skill/add', methods=['POST'])
def add_skill():
    if 'user' not in session:
        return redirect(url_for('login'))

    skill_name = request.form.get('skill_name')
    if skill_name:
        new_skill = Skill(name=skill_name)
        db.session.add(new_skill)
        db.session.commit()

    return redirect(url_for('dashboard_profile'))

@app.route('/dashboard/profile/skill/delete/<int:id>', methods=['POST'])
def delete_skill(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()

    return redirect(url_for('dashboard_profile'))

@app.route('/dashboard/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)