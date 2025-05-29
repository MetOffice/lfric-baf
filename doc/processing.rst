BAF Processing
==============

This chapter describes the processing of an application script
by the BAF base class.
The knowledge of this process will indicate how a derived, application-specific
build script can overwrite methods to customise the build process.

The full class documentation is at the end of this chapter.

The constructor sets up ultimately the Fab ``BuildConfig`` for the build.
It takes two arguments - the name of the application, and
optional the name of the root symbol for a binary to be compiled,
i.e. the program name of a Fortran Program unit. If no
root symbol is specified, the name will be used as root symbol.

The actual build is then started calling the ``build`` method
of the created script. A typical outline of a BAF-based build script is
therefore::

    from baf_base import BafBase

    class ExampleBuild(BafBase):
        # Additional methods to be overwritten or added

    if __name__ == '__main__':
        # Adjust logging level as appropriate
        logger = logging.getLogger('fab')
        logger.setLevel(logging.DEBUG)
        example = ExampleBuild(name="example")
        example.build()

The two main steps, construction and building, are described next.

Constructor
-----------
As mentioned, the constructor will ultimately create the Fab
``BuildConfig`` object, which is then used to compile the
application. The setup of this ``BuildConfig`` can be
modified by overwriting the appropriate methods in a derived class,
and site- and platform-specific setup can be done in a site-
and platform-specific configuration script.

.. _site_and_platform:

Defining ``site`` and ``platform``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The method ``define_site_platform_target()`` is first called.
This method parses the arguments provided by the user and looks
only for the options ``--site`` and ``--platform`` - any other
option is for now ignored. These two arguments are then used
to define a ``target`` attribute, which is either ``default``
or in the form ``{site}_{platform}``. This name is used to
identify the directory that contains the site-specific
configuration script to be executed. The following three
property getters can be used to access the values:

.. autoproperty:: baf_base.BafBase.platform
    :noindex:
.. autoproperty:: baf_base.BafBase.site
    :noindex:
.. autoproperty:: baf_base.BafBase.target
    :noindex:

Site-specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~
After defining the site and platform, a site- and platform-specific
configuration script is executed (if available). BAF will try to 
import a module called ``config`` from the path specified with
the target name (see :ref:`above<site_and_platform>`).
If this is successful, it creates an instance of the ``Config``
class from the module. This all happens here:

.. automethod:: baf_base.BafBase.site_specific_setup
    :noindex:

Remember if no site- and no platform-name is specified,
it will import the ``Config`` class from the directory
called ``default``. 

Chapter :ref:`site_specific_config`
describes this class in more detail. An example for the usage
of site-specific configuration is to add new compilers to
Fab's ``ToolRepository``, or set the default compiler suite for
a site.

.. _define_command_line_options:

Defining command line options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After executing the site-specific configuration file, a Python
argument parser is created with all command line options in the
method ``define_command_line_options``:

.. automethod:: baf_base.BafBase.define_command_line_options
    :noindex:

This method can be overwritten if an application want to add
additional command line flags. The method gets an optional
Python ``ArgumentParser``: a derived class might want to
provide its own instance to provide a better description
message for the argument parser's help message. See
:ref:`here<better_help_messages>` for an example.

A special case is the definition of compilation profiles (like
``fast-debug`` etc). BAF will query the site-specific configuration
object using ``get_valid_profiles()`` to receive a list of all
valid compilation profile names. This allows each site to
specify its own profile modes.

Parsing command line options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once all command line options are defined in the parser,
the parsing of the command line options happens in:

.. automethod:: baf_base.BafBase.handle_command_line_options
    :noindex:

The result of the parsing is stored in an attribute, which can
be accessed using the ``args`` property of the BAF script.

Again, this method can be overwritten to handle the added
application-specific command line options. 

Once the application's ``handle_command_line_options`` has been
executed, the method with the same name in the site-specific
config file will also be called. It gets the argument namespace
information from Python's ArgumentParser as argument:

.. automethod:: default.config.Config.handle_command_line_options
    :noindex:

This can be used for further site-specific modifications, e.g.
it might add additional flags for the compiler or linker. 
:ref:`handling_new_command_line_options` shows an example of
doing this.

``BuildConfig`` creation
~~~~~~~~~~~~~~~~~~~~~~~~
After parsing the command line options, BAF will first
create a Fab ``ToolBox`` which contains the compiler and
linker selected by the user (see Fab documentation for
details). Then it will create the ``BuildConfig`` object,
providing the ``ToolBox`` and the appropriate command line
options::

    label = f"{name}-{self.args.profile}-$compiler"
    self._config = BuildConfig(tool_box=self._tool_box,
                               project_label=label,
                               verbose=True,
                               n_procs=self.args.nprocs,
                               mpi=self.args.mpi,
                               openmp=self.args.openmp,
                               profile=self.args.profile,
                               )

.. note:: There is a TODO
    (https://github.com/MetOffice/lfric-baf/issues/52) which will 
    allow an application the option to design its own naming scheme.


Building
--------

grab_files_step
~~~~~~~~~~~~~~~
find_source_files_step
~~~~~~~~~~~~~~~~~~~~~~
c_pragma_injector
~~~~~~~~~~~~~~~~~
define_preprocessor_flags
~~~~~~~~~~~~~~~~~~~~~~~~~
preprocess_c_step
~~~~~~~~~~~~~~~~~
preprocess_fortran_step
~~~~~~~~~~~~~~~~~~~~~~~
analyse_step
~~~~~~~~~~~~
compile_c_step
~~~~~~~~~~~~~~
compile_fortran_step
~~~~~~~~~~~~~~~~~~~~
archive_objects
~~~~~~~~~~~~~~~
link_step
~~~~~~~~~


Full Baf Documentation
----------------------
Here the full documentation of the BAF base class:

.. autoclass:: baf_base.BafBase
    :members:
