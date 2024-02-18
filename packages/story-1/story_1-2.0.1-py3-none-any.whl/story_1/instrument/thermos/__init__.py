

'''

'''

from flask import Flask, request
import json
from os.path import dirname, join, normpath
import os

import traceback

import story_1.instrument.moves as moves

import rich

import story_1.instrument.thermos.routes.home.get as get_home_route

def build (
	records = 1
):
	print ("starting instrument flask service")

	app = Flask (__name__)

	@app.route ("/", methods = [ 'GET' ])
	def route_GET ():
		return get_home_route.present ()	

	@app.route ("/example", methods = [ 'GET' ])
	def route_GET_example ():
		return get_home_route.present ()

	@app.route ("/", methods = [ 'PATCH' ])
	def route ():
		data = ""
		
		print ("A patch request was received.")
		
		try:
			data = request.get_data ();
			
			UTF8 = data.decode ('utf-8')
			if (records >= 1): print ("UTF8 ::", UTF8)
			
			JSON = json.loads (UTF8)
			if (records >= 1): print ("JSON ::", json.dumps (UTF8))
			
			data = moves.play (JSON = JSON)
			if (records >= 1): rich.print_json (data = data)
			
			response = app.response_class (
				response = json.dumps (data),
				status = 200,
				mimetype = 'application/json'
			)

			return response
			
		except Exception as E:
			print ("exception:", traceback.format_exc ())
	
		return json.dumps ({
			"obstacle": ""
		})
	
	return app;