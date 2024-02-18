
'''
	import story_1.belt.monetary.cards.insert as insert_card
	monetary_connection = insert_card.start ()
'''

import pymongo
import story_1.belt.monetary.connect as monetary_connect

def start ():
	monetary_connection = monetary_connect.start ()
	pouch = monetary_connection ["pouch"]
	cards = monetary_connection ["cards"]

	cards.insert_one ({
		"public": {
			"hexadecimal string": ""
		},
		"private": {
			"hexadecimal string": ""
		},
		"seed": {
			"hexadecimal string": ""
		}
	})

	return;