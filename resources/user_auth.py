from flask_restful import Resource, reqparse
from models.users import UserModel, AccessModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=False)
    parser.add_argument('password', type=str, required=False)
    parser.add_argument('group', type=str, required=True, help="This field is mandatory")
    parser.add_argument('code', type=int, required=False)

    def get(self):
        users = UserModel.find_user_details('all')
        return {'Users':[user.json() for user in users]}

    def put(self):
        data = UserRegister.parser.parse_args()
        msg = ''

        if data['username'] :
            user = UserModel.find_user_details(data['username'])
            if user:
                if data['password'] : user.password = data['password']
                #if data['group'] : 
                user.access = data['group']
            else:
                user = UserModel(**data)
            try:
                user.save_to_db()
            except:
                return {'message':"Please recheck the entries."},400
            msg += "User has been created/updated."

        if data['code']:
            priv = AccessModel.get_priviledges(data['group'])
            if priv :
                priv.access_granted = data['code']
            else:
                priv = AccessModel(data['group'], data['code'])
            try:
                priv.add_to_db()
            except:
                return {'message':"Please check 'group' or 'code' value."},400
            msg += "Group has been created/updated."

        return {"message":msg},200

    def delete(self):
        data = UserRegister.parser.parse_args()
        #msg = ''

        if data['username'] :
            user = UserModel.find_user_details(data['username'])
            if user :
                user.delete_user()
               # msg += 'User is deleted.'
            else:
                return {'message':'No such user exist.'},404

        if data['group']:
            AccessModel.get_priviledges(data['group']).del_from_db()

        return {'message':'Record has been deleted successfully.'},200
