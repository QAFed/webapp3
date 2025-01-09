from flask import Flask, render_template, request, jsonify
from db_mod import db, VMdata, Modif


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbadmin:dbadmin@db_service/dbvm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    vm_data = VMdata.query.all()
    return render_template('index.html', vm_data=vm_data)

@app.route('/update', methods=['POST'])
def update_ip_table():
    if not request.is_json:
        return jsonify({'error':'Request must be json'}), 400

    Modif.add_name_from_ip(request.get_json())

    return jsonify({'message': 'Success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
