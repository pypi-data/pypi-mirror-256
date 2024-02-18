
'''
	
'''

'''
	create_belt
	
	fields {
		"label": ""
	}
'''



import story_1.belt.climate as belt_climate

import os
from os.path import dirname, join, normpath
import pathlib
import sys

def play (fields):

	'''
	import story_1.belt.climate as belt_climate
	belt_climate.build (CWD)

	import story_1.belt.monetary as mongo_node
	mongo_node.start (
		param = {
			"directory": "",
			"port": "27107"
		}
	)
	'''

	offline_climate = belt_climate.retrieve ()
	belts_paths = offline_climate ["paths"] ["belt"]
	
	if ("label" not in fields):
		return {
			"victory": "no",
			"alarm": {
				"string": f'Please choose a "label" for the belt.'
			}
		}
	
	belt_label = fields ["label"]
	belt_path = str (normpath (join (belts_paths, belt_label)))

	if (os.path.isdir (belt_path) != True):
		os.mkdir (belt_path)
		belt_climate.climate ["elected belt"] ["path"] = belt_path
		return {
			"victory": "yes",
			"details": {
				"string": "belt created"
			}
		}
		
	else:
		belt_climate.climate ["elected belt"] ["path"] = belt_path
		return {
			"victory": "no",
			"alarm": {
				"string": "There is already a directory at that path"
			}
		}
