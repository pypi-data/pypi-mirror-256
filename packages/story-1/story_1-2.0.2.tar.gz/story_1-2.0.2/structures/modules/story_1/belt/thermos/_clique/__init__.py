



import story_1.belt.thermos.start_dev as flask_start_dev
import story_1.belt.moves as belt_moves

import atexit
import os
from os.path import dirname, join, normpath
import pathlib
import sys
		
		
def add ():
	import click
	@click.group ("thermos")
	def group ():
		pass

	'''
		belt thermos start --label belt_1 --service-port 50000 --mongo-port 50001
	'''
	import os
	import click
	@group.command ("start")
	@click.option ('--name', default = 'belt')
	@click.option ('--thermos-port', '-sp', default = '50000')
	@click.option ('--mongo-port', '-mp', default = '50001')
	def start (name, thermos_port, mongo_port):
		def stop ():
			print ("--")
			print ("thermos start atexit!");
			print ("--")

		def stop_2 ():
			print ("--")
			print ("thermos start atexit 2!");
			print ("--")
		
		atexit.register (stop)
		atexit.register (stop_2)
		
		'''
			This might only work if this is called:
				process.wait () 
		'''
		
	
		CWD = os.getcwd ();
		effect = belt_moves.perform (
			move = {
				"name": "start thermos",
				"fields": {
					"CWD": CWD,
					"name": name,
					"thermos port": thermos_port,
					"mongo port": mongo_port
				}
			}
		)
	
		print ("effect:", effect)
	
		return;
	
		'''
		import sys
		from os.path import dirname, join, normpath
		import pathlib
		CWD = os.getcwd ();
		mongo_DB_directory = str (normpath (join (CWD, label, "mongo_DB_directory")))
		belt_path = str (normpath (join (CWD, label)))
		
		import story_1.belt.climate as belt_climate
		belt_climate.build (
			belt_path = belt_path
		)
		
		if (not os.path.exists (mongo_DB_directory)):			
			os.mkdir (mongo_DB_directory) 
			
		if (not os.path.isdir (mongo_DB_directory)):
			print ("There is already something at:", mongo_DB_directory)
			return;
		
		from multiprocessing import Process
		
		import story_1.belt.monetary as belt_mongo
		mongo = Process (
			target = belt_mongo.start,
			args = (),
			kwargs = {
				"params": {
					"DB_directory": mongo_DB_directory,
					"port": str (mongo_port)
				}
			}
		)
		mongo.start ()
	

		flask_server = Process (
			target = flask_start_dev.start,
			args = (),
			kwargs = {
				"port": service_port
			}
		)
		flask_server.start ()
		
	
		import time
		while True:
			time.sleep (1000)
		'''
		
		return;


	'''
		belt thermos create_safe --label belt-1
	'''
	import click
	@group.command ("create_safe")
	@click.option ('--label', required = True)
	@click.option ('--port', '-np', default = '50000')
	def create_safe (label, port):	
		address = f"http://127.0.0.1:{ port }"
	
		import json
		from os.path import dirname, join, normpath
		import os
		import requests
		r = requests.patch (
			address, 
			data = json.dumps ({
				"label": "create safe",
				"fields": {
					"label": label
				}
			})
		)
		print (r.text)
		
		return;
		
	return group




#



