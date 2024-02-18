
'''
	
'''

'''
	create_instrument
	
	fields {
		"label": ""
	}
'''



import story_1.instrument.climate as instrument_climate

import os
from os.path import dirname, join, normpath
import pathlib
import sys

def play (fields):

	'''
	import story_1.instrument.climate as instrument_climate
	instrument_climate.build (CWD)

	import story_1.instrument.monetary as mongo_node
	mongo_node.start (
		param = {
			"directory": "",
			"port": "27107"
		}
	)
	'''

	offline_climate = instrument_climate.retrieve ()
	instruments_paths = offline_climate ["paths"] ["instrument"]
	
	if ("label" not in fields):
		return {
			"obstacle": f'Please choose a "label" for the instrument.'
		}
	
	instrument_label = fields ["label"]
	instrument_path = str (normpath (join (instruments_paths, instrument_label)))

	if (os.path.isdir (instrument_path) != True):
		os.mkdir (instrument_path)
		instrument_climate.climate ["elected instrument"] ["path"] = instrument_path
		return {
			"victory": "instrument created"
		}
		
	else:
		instrument_climate.climate ["elected instrument"] ["path"] = instrument_path
		return {
			"obstacle": "There is already a directory at that path"
		}
