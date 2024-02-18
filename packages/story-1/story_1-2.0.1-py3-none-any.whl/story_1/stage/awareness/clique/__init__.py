



import os
	
import rich
		
import story_1.stage.moves as stage_moves

def start ():
	import click
	@click.group ("stage")
	def group ():
		pass

	'''
		stage make --thermos-port 56700 --mongo-port 56701
	'''
	import click
	@group.command ("make")
	@click.option ('--thermos-port', '-tp', default = '55500')
	@click.option ('--mongo-port', '-mp', default = '55501')
	@click.option ('--name', default = 'stage')
	def search (thermos_port, mongo_port, name):	
		CWD = os.getcwd ();
	
		effect = stage_moves.perform (
			move = {
				"name": "make",
				"fields": {
					"CWD": CWD,
					"name": name,
					"thermos port": "",
					"mongo port": ""
				}
			}
		)
		
		rich.print_json (data = effect)
	
		return;

	return group




#



