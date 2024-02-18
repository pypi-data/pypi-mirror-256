




from .group import clique as clique_group

def clique ():
	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("sphene")
	def open_sphene ():	
		import pathlib
		from os.path import dirname, join, normpath
		this_folder_path = pathlib.Path (__file__).parent.resolve ()
		this_module_path = normpath (join (this_folder_path, ".."))

		import sphene
		sphene.start ({
			"extension": ".s.HTML",
			"directory": str (this_module_path),
			"relative path": str (this_module_path)
		})

		import time
		while True:
			time.sleep (1000)


	import click
	@click.command ("example")
	def example_command ():	
		print ("example")

	group.add_command (example_command)
	group.add_command (open_sphene)

	group.add_command (clique_group ())
	group ()




#
