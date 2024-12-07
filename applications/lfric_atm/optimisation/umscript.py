
'''
PSyclone transformation script for a generic transformation of a UM
file. This transformation just adds a comment at the top of the file.

'''

from psyclone.psyir.nodes import FileContainer


def trans(file_container):
    '''Just adds a comment to the file to show that the file was processed.

    '''
    if isinstance(file_container, FileContainer):
        # This is current PSyclone trunk. The transformation receives a
        # PSyIR FileContainer, and has convenient functions to add comments:
        file_container.append_preceding_comment("Processed by umscript.py")
        file_container.append_preceding_comment("------------------------")
        file_container.append_preceding_comment("")
    else:
        # PSyclone 2.5. This needs a bit more wrangling to get PSyIR
        # and to add a comment. First of all, we get a NemoPSY
        # object, not a file container:
        file_container = file_container.container

        # And you can easily only set a single comment:
        file_container.preceding_comment = "Processed by umscript.py"

    # Obviously, you can do any other transformation here.
