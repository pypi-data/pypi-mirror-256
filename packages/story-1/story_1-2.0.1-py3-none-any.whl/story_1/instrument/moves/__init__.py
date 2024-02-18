

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

import os
from os.path import dirname, join, normpath

import story_1.instrument.moves.names.make as make
import story_1.instrument.moves.names.form_proposal_keys as form_proposal_keys
import story_1.instrument.moves.names.start_thermos as start_thermos

moves = {
	"make": make.play,
	"start thermos": start_thermos.perform,
	
	"form proposal keys": form_proposal_keys.play
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
		return moves [ name ] (move ["fields"])

	return {
		"obstacle": {
			"string": f'A move named "{ name }" was not found.',
			"moves": moves
		}
	}
