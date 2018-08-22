# # load cobverted gml file; either json or gexf and push the data to Firestore
# # /processed/ folder
#
# # TODO: make file paths relative
# # TODO: move keyfile?
#
# # import modules
import json
# import uuid
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
#
# cred = credentials.Certificate('backend/keyfile.json')
# default_app = firebase_admin.initialize_app(cred)
#
# db = firestore.client()
# doc_ref = db.collection(u'network').document(u'thedatafox')
# doc_ref.set(
#
#
#
# with open('../../data/processed/TheDataFox.json.json') as data_file:
#
# #
# # for artist in artists:
# #     artist["id"] = str(uuid.uuid4())
# #     doc_ref = db.collection(u'artists').document(artist["id"])
# #     doc_ref.set(artist)
#
#

parsed = json.loads('../../../data/processed/TheDataFox.json')
print(json.dumps(parsed, indent=4, sort_keys=True))