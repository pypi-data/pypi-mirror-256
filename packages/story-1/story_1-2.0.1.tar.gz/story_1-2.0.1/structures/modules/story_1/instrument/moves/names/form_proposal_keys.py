
'''
	{
		"label": "form proposal keys",
		"fields": {
			"seed": ""
		}
	}
'''

import story_1.instrument.climate as instrument_climate

def play (fields):
	paths = instrument_climate ["paths"]

	seed = fields ["seed"]
	directory_path = fields ["directory_path"]

	print (
	
	)

	import story_1.modules.proposals.keys.form as form_proposal_keys
	form_proposal_keys.smoothly (
		#
		#	inputs, consumes, utilizes
		#
		utilizes = {
			"seed": seed
		},
		
		#
		#	outputs, produces, builds
		#
		builds = {
			"seed": {
				"path": normpath (join (directory_path, "proposal.seed"))
			},
			"private key": {
				"format": "hexadecimal",
				"path": normpath (join (directory_path, "proposal.private_key.hexadecimal"))
			},
			"public key": {
				"format": "hexadecimal",
				"path": normpath (join (directory_path, "proposal.public_key.hexadecimal"))
			}
		}
	)