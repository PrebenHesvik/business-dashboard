from sqlalchemy import Table, text
from sqlalchemy.orm.session import sessionmaker
from werkzeug.security import generate_password_hash
from app import db, engine


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


User_tbl = Table("user", User.metadata)


def create_user_table():
    User.metadata.create_all(engine)


def add_user(email, password):
    hashed_password = generate_password_hash(password, method="sha256")
    ins = User_tbl.insert().values(email=email, password=hashed_password)
    with engine.connect() as conn:
        conn.execute(ins)


def del_user(email):
    delete = User_tbl.delete().where(User_tbl.c.email == email)
    with engine.connect() as conn:
        conn.execute(delete)


def show_users():
    with engine.connect() as conn:
        results = conn.execute(text('SELECT email FROM user')).fetchall()
        results = [result.email for result in results]
        return results


def show_users2():
    Session = sessionmaker(bind=engine)
    session = Session()

    results = [instance.email for instance in session.query(User)]
    session.close()

    return results
