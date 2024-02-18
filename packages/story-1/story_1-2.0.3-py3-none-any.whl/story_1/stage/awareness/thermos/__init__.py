



import story_1.belt.awareness.thermos.start_dev as flask_start_dev

def clique ():
	import click
	@click.group ("thermos")
	def group ():
		pass

	'''
		stage thermos start --port 60000
	'''
	import click
	@group.command ("start")
	@click.option ('--port', '-p', default = '55500')
	def search (port):		
		flask_start_dev.start (
			port = int (port)
		)
	
		return;

	return group




#



