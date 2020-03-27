from flask_restful import Resource, reqparse
from models.rules import RuleModel
from models.network import NetworkModel

class ACL(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('dl_src', required=False)
    parser.add_argument('dl_dst', required=False)
    parser.add_argument('nw_src', required=False)
    parser.add_argument('nw_dst', required=False)
    parser.add_argument('nw_proto', required=False)
    parser.add_argument('tp_src', required=False)
    parser.add_argument('tp_dst', required=False)
    parser.add_argument('actions', required=False)

    def get(self, role, device):
        if role == 'switch':
            return {'message':'This feature is not applicable for switches.'},400
        elif NetworkModel.fetch_db(role, device):
            rules = RuleModel.get_rules(device)
            if rules:
                return {'rules':[rule.json() for rule in rules]},201
            return {'message':'No rule present for this device'},201
        return {'message':'No such device present with name {}.'.format(device)},404


    def post(self, role, device): 
        if NetworkModel.fetch_db(role, device):
            rule = ACL.parser.parse_args()
            if RuleModel.get_rules(device, **rule):
                return {'message':'Rule already exit for the device.'},400
            RuleModel(device, **rule).save_to_db()
            return {'message':'Rule successfully added.'}
            
        return {'message':'{} device do not exist.'.format(device)},404


    def delete(self, role, device):
        if role == 'switch':
            return {'message':'No rule(s) exist for switch.'},400
        elif NetworkModel.fetch_db(role, device):
            del_rule = ACL.parser.parse_args()
            rules = RuleModel.get_rules(device, **del_rule)
            if rules:
                for rule in rules:
                    rule.delete_from_db()
                return {'message':'Rule is deleted.'},201
            else:
                return {'message':'No rule exist. Please check inputs.'},400

