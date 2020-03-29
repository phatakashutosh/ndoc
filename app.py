from flask import Flask
from flask_restful import Api

from resources.network_core import Network
from resources.rule_core import ACL
from resources.user_auth import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sql123@localhost/network'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

api = Api(app)

api.add_resource(Network, '/network/status/<string:role>')
api.add_resource(ACL, '/network/rules/<string:role>/<string:device>')
api.add_resource(UserRegister, '/network/users')

if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(host='10.2.0.3', port=5000, debug=False, use_debugger=False)
