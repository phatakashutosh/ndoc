from db import db

class UserModel(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(15), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    access = db.Column(db.String(10), db.ForeignKey('priviledges.access_group'))

    priv = db.relationship('AccessModel')
    

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.access = kwargs['group']

    def json(self):
        return {'username':self.username, 'password':self.password, 'group':self.access}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_user_details(cls, username):
        if username == 'all':
            return cls.query.all()
        return cls.query.filter_by(username=username).first()

class AccessModel(db.Model):
    __tablename__ = "priviledges"
    access_group = db.Column(db.String(10), primary_key=True)
    access_granted = db.Column(db.Integer, nullable=False)
    users = db.relationship('UserModel')

    def __init__(self, group, code):
        self.access_group = group
        self.access_granted = code

    def json(self):
        return {'access_group':self.access_group}

    @classmethod
    def get_priviledges(cls, group):
        return cls.query.filter_by(access_group=group).first()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def del_from_db(self):
        db.session.delete(self)
        db.session.commit()
