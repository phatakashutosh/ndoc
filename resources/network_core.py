from flask_restful import Resource, reqparse

from models.network import NetworkModel

class Network(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('device_name', required=True, help='This field can not be left blank!')
    parser.add_argument('status', required=False, help='Every device has status')

    def get(self, role):
        devices = NetworkModel.fetch_db(role)
        if devices:
            try:
                return {'devices': [device.json() for device in devices]}
            except:
                return devices.json()
        return {'message':'No data found'},404

    def post(self, role):
        data = Network.parser.parse_args()
        if NetworkModel.fetch_db(role, data['device_name']):
            return {'message':'The device {} is already exist in {}.'.format(data['device_name'],role)},400

        if data['status']:
            device = NetworkModel(data['device_name'], role, data['status'])
        else:
            device = NetworkModel(data['device_name'], role, "not found")
        try:
            device.save_to_db()
        except:
            return {'message':'Could not add device {} in {}. Kindly recheck inputs.'.format(data['device_name'], role)},500
        return device.json()

    def put(self, role):
        data = Network.parser.parse_args()
        device = NetworkModel.fetch_db(role, data['device_name'])

        if device:
            device.status = data['status']
            device.save_to_db()
            return device.json()
        else:
            return {'message':'No device with name {} found in {}.'.format(data['device_name'], role)},404

    def delete(self, role):
        data = Network.parser.parse_args()
        device = NetworkModel.fetch_db(role, data['device_name'])
        if device:
            device.delete_from_db()
            return {'message':'Device {} is removed.'.format(data['device_name'])}
        return {'message':'Device {} is not found in {}.'.format(data['device_name'],role)},404
