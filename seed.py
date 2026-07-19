from app import app, db
from models import Profile, Skill, Project

with app.app_context():
    profile = Profile(
        name="Lesty Amelya",
        headline="Mahasiswa Informatika | Web Designer",
        about="Hi, I'm Lesty! Mahasiswa Teknik Informatika asal Bandung yang jatuh cinta sama coding dan desain." \
        " Aktif explore web development, mobile apps dengan Flutter, dan project Python — " \
        "dengan passion utama di UI/UX design yang clean tapi tetap playful. " \
        "Di luar coding, aku suka menggambar, berkebun, dan selalu penasaran belajar hal baru (sekarang lagi eksplor AI!)." \
        " Website ini adalah cerminan diriku: teknologi yang fungsional dan menyenangkan, dengan sentuhan lucuu di setiap detailnya.",
        photo="profil.jpg",
        email="lestyamelya008@gmail.com",
        github="https://github.com/LestyAmelya-glitch",
        linkedin="https://www.linkedin.com/in/lesty-amelya-ba08b8422/"
    )
    db.session.add(profile)

    skill1 = Skill(name="Python")
    skill2 = Skill(name="Flask")
    skill3 = Skill(name="HTML/CSS")
    skill4 = Skill(name="menggambar(Tadisional/Digital)")
    db.session.add_all([skill1, skill2, skill3, skill4])

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