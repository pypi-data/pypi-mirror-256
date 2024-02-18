

import pathlib
print ("stage @:", pathlib.Path (__file__).parent.resolve ())


import story_1.stage.awareness.clique as clique_intro
def start_clique ():
	group = clique_intro.start ()
	group ()