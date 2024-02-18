


'''
	
'''

'''
	create_belt
	
	fields {
		"label": ""
	}
'''


from multiprocessing import Process

import story_1.belt.climate as belt_climate
import story_1.belt.monetary as belt_mongo

import os
from os.path import dirname, join, normpath
import pathlib
import sys

def perform (move):
	mongo_DB_directory = move ["mongo directory"]
	mongo_port = move ["mongo port"]

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
	
