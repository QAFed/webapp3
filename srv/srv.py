from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbadmin:dbadmin@db_service/dbvm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class VMdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ip = db.Column(db.String(50))

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

@app.route('/')
def index():
    vm_data = VMdata.query.all()
    return render_template('index.html', vm_data=vm_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)