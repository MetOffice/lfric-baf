.. _site_specific_config:

Site-specific Configuration Files
=================================

This chapter describes the design of the site-specific
configuration files. It starts with the concept, and then
includes some examples.

Concepts for site-specific setup
--------------------------------
BAF's support for site-specific setup is based on using a site name
and a platform name. For example, The UK Met Office traditionally
uses ``meto`` as site name, and then a different platform name, e.g.
``xc40`` or ``ex1a``. BAF uses a specific setup directory based on the
concatenation of these names. In the example above, this would be
``meto_xc40`` or ``meta_ex1a``. These names can be specified as command
line option (see :ref:`Command Line Options<command_line_options>`).

If no site name is specified, ``default`` is used. And similarly,
if no platform is specified, ``default`` is also used (resulting
e.g. in ``meto-default`` etc). If neither site nor platform is specified,
the name ``default`` is used.

Default configuration
---------------------
It is strongly recommended for each application to have a default
configuration file, which will define for example compiler profiles,
and typical compiler flags. Any site-specific configuration file
should then inherit from this default, but can then enhance the
setup done by the default.

.. code-block:: python

	from default.config import Config as DefaultConfig
	class Config(DefaultConfig):
	    '''Make intel-classic the default compiler
	    '''
	    def __init__(self):
	        super().__init__()
	        tr = ToolRepository()
	        tr.set_default_compiler_suite("intel-classic")


Callbacks in configuration files
--------------------------------
The BAF base class adds several calls to the site-specific
configuration file, allowing site-specific changes to the build
process. These callbacks are described here.

Constructor
~~~~~~~~~~~
The constructor receives no parameter, and happens rather early in the
BAF processing chain (see :ref:`site_and_platform`), i.e. at a stage
where not even all command line options have been defined. Typically,
the constructor will just 



- defining profiles

