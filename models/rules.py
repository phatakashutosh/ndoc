from db import db

class RuleModel(db.Model):
    __tablename__ = "rules"

    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(10), db.ForeignKey('device_status.device_name'))
    dl_src = db.Column(db.String(20))
    dl_dst = db.Column(db.String(20), nullable=True)
    nw_src = db.Column(db.String(20), nullable=True)
    nw_dst = db.Column(db.String(20), nullable=True)
    nw_proto = db.Column(db.String(10), nullable=True)
    tp_src = db.Column(db.String(10), nullable=True)
    tp_dst = db.Column(db.String(20), nullable=True)
    actions = db.Column(db.String(5), nullable=True)
#    device = db.Column(db.String(10), db.ForgeinKey('device_status.device_name')

    device_status = db.relationship('NetworkModel')

    def __init__(self, device, **kwargs):
        self.device = device
        self.rule = kwargs
        self.dl_src = kwargs['dl_src']
        self.dl_dst = kwargs['dl_dst']
        self.nw_src = kwargs['nw_src']
        self.nw_dst = kwargs['nw_dst']
        self.nw_proto = kwargs['nw_proto']
        self.tp_src = kwargs['tp_src']
        self.tp_dst = kwargs['tp_dst']
        self.actions = kwargs['actions']


    def json(self):
        return {'device_name':self.device, 'rules':{'dl_src':self.dl_src, 'dl_dst':self.dl_dst, 'nw_src':self.nw_src, 'nw_dst':self.nw_dst, 'nw_proto':self.nw_proto, 'tp_src':self.tp_src, 'tp_dst':self.tp_dst, 'actions':self.actions}}


    @classmethod
    def get_rules(cls, device, **kwargs):
        if kwargs:
            return cls.query.filter_by(device=device, **kwargs).all()
        return cls.query.filter_by(device=device).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


