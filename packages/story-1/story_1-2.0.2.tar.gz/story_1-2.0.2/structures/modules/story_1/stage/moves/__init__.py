

'''
	import story_1.stage.moves as stage_moves

	effect = stage_moves.perform (
		move = {
			"name": "",
			"fields": {
				
			}
		}
	)
'''

'''
	
'''

'''
	obstacles: {
		"obstacle": {
			"string": ""
		}
	}
'''
import os
from os.path import dirname, join, normpath

import story_1.stage.moves.names.make as make
import story_1.stage.moves.names.propose_join as propose_join
moves = {
	"make": make.perform,
	
	#
	#	proposals
	#
	"propose join": propose_join.perform
}

def records (record):
	print (record)

def perform (
	move = "",
	records = records
):
	if ("name" not in move):
		records (f'The "name" of the move was not given.')
		return;
	
	name = move ["name"];
	if (name in moves):
		return moves [ move ["name"] ] ()


	return {
		"obstacle": {
			"string": f'A move named "{ name }" was not found.'
		}
	}
