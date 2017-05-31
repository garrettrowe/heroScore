import os
import sys
import traceback
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
	hero = 0
	Efficiencyv = 0
	Mitigationv = 0
	Supportv = 0
	Ultimatev = 0
	Scalingv = 0
	Productionv = 0
	Depthv = 0
	Funv = 0
	DEv = 0	     
	Fights = 0
	try:
		global mpredict
		mpredict = []
		hero = int(request.args.get('Hero'))
		Efficiencyv = float(request.args.get('Efficiencyv'))
		Mitigationv = float(request.args.get('Mitigationv'))
		Supportv = float(request.args.get('Supportv'))
		Ultimatev = float(request.args.get('Ultimatev'))
		Scalingv = float(request.args.get('Scalingv'))
		Productionv = float(request.args.get('Productionv'))
		Depthv = float(request.args.get('Depthv'))
		Funv = float(request.args.get('Funv'))
		DEv = float(request.args.get('DEv'))
		Fights = int(request.args.get('Fights'))
	
	except:
		"Fail"
	inpredict = [hero,Efficiencyv,Mitigationv,Supportv,Ultimatev,Scalingv,Productionv,Depthv,Funv,DEv,Fights]
	inpredict = numpy.array(inpredict).reshape(1, (len(inpredict)))
	mscore = regr.predict(inpredict)[0][0]
	mpredict.append({'Score' : mscore})
	return jsonify(results=mpredict)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

