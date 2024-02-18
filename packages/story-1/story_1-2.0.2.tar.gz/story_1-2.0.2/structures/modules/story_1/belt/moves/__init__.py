

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
	returns {
		"victory": "yes"
	}
'''

'''
	returns {
		"victory": "no",
		"alarm": {
			"string": ""
		}
	}
'''

import os
from os.path import dirname, join, normpath

import story_1.belt.moves.names.make as make
import story_1.belt.moves.names.start_thermos as start_thermos
import story_1.belt.moves.names.is_on as is_on

#
#	cards
#
import story_1.belt.moves.names.cards.make as make_card
import story_1.belt.moves.names.cards.enumerate as enumerate_cards



moves = {
	"make": make.play,
	"start thermos": start_thermos.perform,
	
	#
	#	is on
	#
	"is on": is_on.perform,
	
	#
	#	cards
	#
	"make card": make_card.perform,
	"enumerate cards": enumerate_cards.perform
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
		"victory": "no",
		"alarm": {
			"string": f'A move named "{ name }" was not found.',
			"details": moves
		}
	}
