# load converted gml file in json format and push to Firebase

# TODO: make file paths relative
# TODO: move keyfile?

# import modules
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

def push_json_firebase():
    # load config # TODO: use dotenv going forward
    with open('../../../twitter-analyzer-app/backend/local.json') as json_local_file:
        config = json.load(json_local_file)

    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('../../../twitter-analyzer-app/backend/keyfile.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://twitteranalyzer-f4bb9-a5664.firebaseio.com/'
    })

    # As an admin, the app has access to read and write all data, regardless of Security Rules
    ref = db.reference('network')
    with open ('../../../data/processed/TheDataFox.json') as node_link_data:
        data = json.load(node_link_data)
        ref.set(data)




