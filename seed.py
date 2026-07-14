from app import app, db
from models import Profile, Skill, Project

with app.app_context():
    profile = Profile(
        name="Lesty Amelya",
        headline="Mahasiswa Informatika | Web Developer",
        about="Saya mahasiswa yang sedang belajar membangun aplikasi web dengan Python dan Flask.",
        photo="profil.jpg",
        email="emailkamu@gmail.com",
        github="https://github.com/username-kamu",
        linkedin="https://linkedin.com/in/username-kamu"
    )
    db.session.add(profile)

    skill1 = Skill(name="Python")
    skill2 = Skill(name="Flask")
    skill3 = Skill(name="HTML/CSS")
    db.session.add_all([skill1, skill2, skill3])

    project1 = Project(
        title="Website Toko Online Sederhana",
        description="Aplikasi e-commerce sederhana untuk belajar CRUD dan autentikasi menggunakan Flask.",
        technologies="Python, Flask, SQLite",
        image_file="default.jpg",
        github_link="https://github.com/username-kamu/toko-online",
        live_link=""
    )
    project2 = Project(
        title="Aplikasi To-Do List",
        description="Aplikasi pencatat tugas harian dengan fitur tambah, edit, dan hapus tugas.",
        technologies="Python, Flask, JavaScript",
        image_file="default.jpg",
        github_link="https://github.com/username-kamu/todo-app",
        live_link=""
    )
    db.session.add_all([project1, project2])

    db.session.commit()
    print("Data berhasil ditambahkan!")