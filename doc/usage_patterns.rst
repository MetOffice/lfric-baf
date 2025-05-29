Common Usage Pattern
====================

Creating a new site and platform
---------------------------------
To define a new site and platform, first create a directory with
the name ``f"{site}_{platform}"`` in the directory in which the
BAF base class is. In this directory, create a file called
``config.py``, which must define a class called ``Config``.

In general, it is recommended that any new config should inherit
from the default configuration (since this will typically provide
a good setup for various compilers). For example::

    from default.config import Config as DefaultConfig

    class Config(DefaultConfig):
        """
        A new site- and platform-specific setup file
        that sets the compiler default for this site to be
        intel-classic.
        """

        def __init__(self):
            super().__init__()
            tr = ToolRepository()
            tr.set_default_compiler_suite("intel-classic")

More methods can be overwritten to allow further customisation.


.. _better_help_messages:

Adding more command line options and better help messages
---------------------------------------------------------
As outlined in :ref:`define_command_line_options`, an
application can implement its own ``define_command_line_options``
method. An example which adds a new ``revision`` flag::

    class JulesBuild(BafBase):

        def define_command_line_options(self,
                                        parser: Optional[ArgumentParser] = None
                                        ) -> ArgumentParser:
            """
            :param parser: optional a pre-defined argument parser. If not, a
                new instance will be created.
            """
            parser = super().define_command_line_options(parser)
            parser.add_argument(
                "--revision", "-r", type=str, default="vn7.8",
                help="Sets the Jules revision to checkout.")
            return parser

Since the Python argument parser also allows specification of
a help message, this example can be extended as follows to provide
a better message::

    import argparse

    class JulesBuild(BafBase):

        def define_command_line_options(self,
                                        parser: Optional[ArgumentParser] = None
                                        ) -> ArgumentParser:
            """
            :param parser: optional a pre-defined argument parser. If not, a
                new instance will be created.
            """

            # Allow another derived class to provide its own parser (with its
            # own description message). If not, create a parser with a better
            # description:
            if not parser:
                parser = argparse.ArgumentParser(
                    description=("A BAF-based build system for Jules."),
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

            super().define_command_line_options(parser)
            parser.add_argument(
                "--revision", "-r", type=str, default="vn7.8",
                help="Sets the Jules revision to checkout.")
            return parser

.. _handling_new_command_line_options:

Handling a new command line option
----------------------------------
As indicated in :ref:`define_command_line_options`, the method
``handle_command_line_options`` can be overwritten to handle
newly added command line options. Extending the previous
examples of a Jules build script, here is how the revision of
Jules is stored and then used::

    class JulesBuild(BafBase):

        def handle_command_line_options(self, parser):
            """
            Grab the requested (or default) Jules revision to use and
            store it in an attribute.
            """

            super().handle_command_line_options(parser)
            self._revision = self.args.revision

        def grab_files(self):
            """
            Extracts all the required source files from the repositories.
            """
            git_checkout(
                self.config,
                src="git@github.com:MetOffice/jules",
                revision=self._revision)

Strictly speaking, it is not necessary to store a command line option
that is already included in ``args`` as a separate attribute as shown
above - after all, the revision parameter could also be taken from
``self.args.revision`` instead. It is only done to make the code a little
bit easier to read, and make this part of the code independent of the
naming of the command line argument. If at some stage the command line
option for the Jules revision needs to be changed, the actual extract
step would not need to be changed.

