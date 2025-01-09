from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class VMdata(db.Model):
    __tablename__ = 'ip_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ip = db.Column(db.String(50))

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip