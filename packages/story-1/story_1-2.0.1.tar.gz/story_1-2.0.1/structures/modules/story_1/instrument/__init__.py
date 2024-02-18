

import pathlib
print ("story 1 @:", pathlib.Path (__file__).parent.resolve ())


import story_1.instrument.awareness.clique as clique_intro
def start_clique ():
	group = clique_intro.start ()
	group ()