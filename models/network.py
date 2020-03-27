from db import db

class NetworkModel(db.Model):
    __tablename__ = 'device_status'
    device_name = db.Column(db.String(10), nullable=False, primary_key=True)
    role = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(10), nullable=False)
    rules = db.relationship('RuleModel', lazy='dynamic')

    def __init__(self, device_name, role, status):
        self.device_name = device_name
        self.role = role
        self.status = status

    def json(self):
        return {'device_name':self.device_name, 'role':self.role, 'status':self.status}

    @classmethod
    def fetch_db(cls, role, name=None):
        if name == None:
            if role == 'all':
                return cls.query.all()
            return cls.query.filter_by(role=role).all()
        return cls.query.filter_by(role=role, device_name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

