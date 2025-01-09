from flask import Flask, render_template
from db_mod import db, VMdata


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbadmin:dbadmin@db_service/dbvm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    vm_data = VMdata.query.all()
    return render_template('index.html', vm_data=vm_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
