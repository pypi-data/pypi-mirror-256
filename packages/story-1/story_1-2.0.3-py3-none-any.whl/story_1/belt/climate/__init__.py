
'''
	import story_1.belt.climate as belt_climate
	climate = belt_climate.retrieve ()
'''

import os
from os.path import dirname, join, normpath
import pathlib
import sys


climate = {
	"elected belt": {},
	"paths": {
		"frontend dist": str (
			normpath (join (
				pathlib.Path (__file__).parent.resolve (), 
				"../frontend"
			))
		)
	}
}

def build (
	belt_path = None
):		
	if (os.path.isdir (belt_path) != True):
		os.mkdir (belt_path)
		print ("The belt was made.")
	else:
		print ()
		print ("There's already something at the path of the belt.")
		print (belt_path)
		print ()

	#climate ["paths"] ["offline_good"] = offline_goods
	climate ["paths"] ["belt"] = belt_path
	

	return;


def retrieve ():
	return climate