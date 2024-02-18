




import os

import story_1.belt.awareness.sockets.clique_group as clique_group
import story_1.belt.thermos._clique as _clique

import story_1.stage.moves as stage_moves


def start ():
	import click
	@click.group ()
	def group ():
		pass
	
	
	'''
		belt sockets --port 65000
	'''
	import click
	@group.command ("make")
	@click.option ('--thermos-port', '-tp', default = '10000')
	@click.option ('--mongo-port', '-mp', default = '10001')
	@click.option ('--name', default = 'belt-1')
	def search (thermos_port, mongo_port, name):	
		CWD = os.getcwd ();
		effect = stage_moves.perform (
			move = {
				"name": "make",
				"fields": {
					"CWD": CWD,
					"name": name,
					"thermos port": thermos_port,
					"mongo port": mongo_port
				}
			}
		)
		
			

		return;
		
		
	
	group.add_command (clique_group.add ())
	group.add_command (_clique.add ())
	
	
	
	#group.add_command (belt_clique_tracks ())
	#group.add_command (belt_clique_socket ())
	#group.add_command (stage_clique ())
	
	#group ()
	
	return group




#
