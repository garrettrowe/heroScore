import os
import sys
import numpy
import threading
from flask import Flask, jsonify, request, json
import swiftclient
from sklearn import linear_model
from sklearn.externals import joblib
import requests
import dateutil.parser

from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app)

conn = swiftclient.Connection(key="""ApX1Y]C*#tvNn95j""",authurl='https://identity.open.softlayer.com/v3',auth_version='3',
os_options={"project_id": 'c103edd6ab074e8f967770017c08c779',"user_id": '70b92ab4ed014fe0b3564f31a53b6522',"region_name": 'dallas'})
obj_tuple = conn.get_object("Analytics", 'super_hero_model_regr.gz')

with open('super_hero_model_regr.gz', 'w') as dl_model:
    dl_model.write(obj_tuple[1])

regr = joblib.load('super_hero_model_regr.gz')

@app.route('/')
def notice():
	return "This is a webapp"

@app.route('/score', methods=['GET', 'POST'])
def parse_request():
	try:
		global mpredict
		mpredict = []
		inpredict = [54,6.3,7.38,4.44,0.45,.05,3.15,0.45,3.33,17.4,35]
		inpredict = numpy.array(inpredict).reshape(1, (len(inpredict)))
		mscore = regr.predict(inpredict)[0][0]
		mpredict.append({'Score' : mscore})
		return jsonify(results=mpredict)
	except:
		return jsonify(ecode=sys.exc_info()[0])

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

