










def clique ():
	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("check-equality")
	@click.option ('--dir-1', required = True)
	@click.option ('--dir-2', required = True)
	def check_dir_equality (dir_1, dir_2):
		import ships.paths.directory.check_equality as check_equality
		report = check_equality.start (
			dir_1,
			dir_2
		)	
		
		rich.print_json (data = { "report": report })
		
		assert (
			report ==
			{'1': {}, '2': {}}
		), report
		
	group.add_command (check_dir_equality)	

	group ()




#
