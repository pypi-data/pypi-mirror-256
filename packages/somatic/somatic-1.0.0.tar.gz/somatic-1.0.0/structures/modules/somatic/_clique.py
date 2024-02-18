

import os
import time
import json
# os.getcwd()

import somatic
import somatic.climate as climate
import somatic.modules.parse_extensions as parse_extensions

def clique ():

	#print ('starting clique')

	import click
	@click.group (invoke_without_command = True)
	@click.pass_context
	def group (ctx):
		if ctx.invoked_subcommand is None:
			#click.echo ('Clique was invoked without a subcommand.')
			start ([], standalone_mode = False)
		else:
			#click.echo ('Clique was invoked with the subcommand: %s' % ctx.invoked_subcommand)
			pass;
	
		pass

	
	

	'''
		somatic somatic --extensions [.s.HTML,.jpg,.png]
		somatic somatic --extensions "[ .s.HTML, .jpg, .png ]"
	'''
	import click
	@click.command ("somatic")
	@click.option ('--extensions', default = None)
	@click.option ('--port', default = 6789)
	@click.option ('--static-port', is_flag = True, default = False)
	@click.option ('--verbose', default = 1)
	def internal_start (extensions, port, static_port, verbose):
		#print ("somatic")
		#print ("extensions:", type (extensions), extensions)
		
		parsed_extensions = parse_extensions.start (extensions);
		
		
	
		print ("parsed exetnsions:", parsed_extensions)
	
		import pathlib
		from os.path import dirname, join, normpath
		this_dir = str (pathlib.Path (__file__).parent.resolve ())
	
		somatic.start ({
			"directory": this_dir,
			"relative path": this_dir,
			
			"port": port,
			"static port": static_port,
			"verbose": verbose,
			
			"extensions": parsed_extensions
		})
		
		# close = input ("press close to exit") 
		while True:                                  
			time.sleep (1)  

	'''
		somatic start --port 2345 --static-port
	'''
	import click
	@click.command ("start")
	@click.option ('--extensions', default = None)
	@click.option ('--port', default = 2345)
	@click.option ('--static-port', is_flag = True, default = False)
	def start (extensions, port, static_port):	
		parsed_extensions = parse_extensions.start (extensions)
	
		somatic.start ({
			"directory": os.getcwd (),
			"relative path": os.getcwd (),
			
			"port": port,
			"static port": static_port,
			"verbose": 1,
			
			"extensions": parsed_extensions
		})
		
		# close = input ("press close to exit") 
		while True:                                  
			time.sleep (1)  

	group.add_command (internal_start)
	group.add_command (start)

	#start ([], standalone_mode=False)

	#group.add_command (clique_group ())
	group ()


	#start ()
	                          
