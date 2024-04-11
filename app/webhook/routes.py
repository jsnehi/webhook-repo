from flask import Blueprint, json, request, render_template,jsonify
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    payload = request.get_json()
    payload_string = json.dumps(payload)
    payload_json = json.loads(payload_string)

    if 'pull_request' in payload_json:
        pull_requests = payload_json['pull_request']
        print(f"{pull_requests=}")
        mongo.db.Requests.insert_one({
            'request_id': pull_requests['id'],
            'author': pull_requests['user']['login'],
            'action': 'PULL_REQUEST',
            'from_branch': pull_requests['head']['ref'],
            'to_branch': pull_requests['base']['ref'],
            'timestamp': datetime.strptime(pull_requests['updated_at'], '%Y-%m-%dT%H:%M:%S%z')
        })
    else:
        if len(payload_json['commits'])==1:
            commit = payload_json['commits'][0]
        else:
            commit = payload_json['commits'][-1]
        
        mongo.db.Requests.insert_one({
            'request_id': commit['id'],
            'author': commit['author']['username'],
            'action': 'PUSH' if len(payload_json['commits']) == 1 else 'MERGE',
            'from_branch': "",
            'to_branch': payload_json['ref'].split("/")[-1],
            'timestamp': datetime.strptime(commit['timestamp'], '%Y-%m-%dT%H:%M:%S%z')
        })
    return {"message":"Added Sucessfully!!"}, 200

@webhook.route('/',methods=["GET"])
def webhook_data():
    data = list(mongo.db.Requests.find({}, {"_id": 0}))
    return render_template('webhook.html', record=data)

@webhook.route('/fetch-data',methods=["GET"])
def fetch_data():
    data = list(mongo.db.Requests.find({}, {"_id": 0}))
    return jsonify(data)
