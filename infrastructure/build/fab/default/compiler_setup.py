#! /usr/bin/env python3

class CompilerSetup:
	'''A baseclass for compiler setup. 
	'''

	_nc_libs = None
    def __init__(self):
    	if CompilerSetup._nc_libs is None:
	        tr = ToolRepository()
        	shell = tr.get_default(Category.SHELL)
        	# We must remove the trailing new line, and create a list:
        	CompilerSetup._nc_flibs = \
        		shell.run(["-c", "nf-config --flibs"]).strip().split()

       def 


