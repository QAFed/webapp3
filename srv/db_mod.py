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

class Modif():
    @staticmethod
    def add_name_from_ip(data_json):
        new_name = data_json.get('name')
        find_ip = data_json.get('ip')
        vm_string = VMdata.query.filter_by(ip=find_ip).first()
        if vm_string:
            vm_string.name = new_name
        else:
            new_vm_string = VMdata(name=new_name, ip=find_ip)
            db.session.add(new_vm_string)
        db.session.commit()







