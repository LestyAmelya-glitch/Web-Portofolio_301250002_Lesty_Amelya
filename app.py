from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Project, Message, Profile, Skill
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['ADMIN_USERNAME'] = 'admin'
app.config['ADMIN_PASSWORD'] = 'admin123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SECRET_KEY'] = 'kunci-rahasia-anda-ganti-nanti'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

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

@app.route('/dashboard/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)