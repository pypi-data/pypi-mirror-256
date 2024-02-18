


'''
	
'''

'''
	create_belt
	
	fields {
		"CWD": CWD,
		"name": name,
		"thermos port": thermos_port,
		"mongo port": mongo_port
	}
'''





import os
from os.path import dirname, join, normpath
import pathlib
import sys
from multiprocessing import Process

from .start_mongo import perform as perform_start_mongo

import story_1.belt.climate as belt_climate
import story_1.belt.thermos.start_dev as flask_dev

import time

def perform (move):
	print ("start thermos");

	assert ("CWD" in move)
	assert ("name" in move)
	assert ("thermos port" in move)
	assert ("mongo port" in move)
	
	name = move ["name"]
	CWD = move ["CWD"]
	thermos_port = move ["thermos port"]
	mongo_port = move ["mongo port"]

	belt_path = str (normpath (join (CWD, name)))
	belt_climate.build (belt_path = belt_path)

	mongo_DB_directory = str (normpath (join (CWD, name, "mongo_DB_directory")))
	if (not os.path.exists (mongo_DB_directory)):			
		os.mkdir (mongo_DB_directory) 
		
	if (not os.path.isdir (mongo_DB_directory)):
		print ("There is already something at:", mongo_DB_directory)
		return;
	
	perform_start_mongo ({
		"CWD": CWD,
		"name": name,
		
		"mongo port": mongo_port,
		"mongo directory": mongo_DB_directory
	});
	
	time.sleep (2)

	flask_server = Process (
		target = flask_dev.start,
		args = (),
		kwargs = {
			"port": thermos_port
		}
	)
	flask_server.start ()
	
	

	while True:
		time.sleep (1000)
