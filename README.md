# LFRic-BAF

This repository contains the current state of BAF, the Build Architecture with
Fab. BAF is an object-oriented command line interface on top of the UK Met Office
build system Fab (https://github.com/MetOffice/fab), which is currently
stored in this repository. It also contains LFRic-BAF, a complete new Fab-based
build system for the UK Met Office's LFRic simulation code.

For now, you need to install this LFRic build system into existing LFRic repositories.
This way, building with Fab can be tested before the new Fab build system becomes
part of the LFRic repos. The documentation here describes how to install the
LFRic build scripts into existing LFRic repositories. This setup has been tested with
gfortran and ifort, this description assumes the usage of gfortran.

## Prerequisites
In order to use the build procedure below, you need to have:

- `gfortran` (`ifort` can also be used, but the instructions here are
  all written for `gfortran`. To use `ifort`, replace `--suite gnu` with
  `-suite intel-classic`, and `gfortran` with `ifort` etc)
- `mpif90` as a compiler wrapper that calls gfortran
- the correct rose-picker version (2.0.0)
- libclang and python-clang
- All lfric dependencies must be available, including:
  - netcdf (including `nf-config`)
  - hdf5
  - xios, yaxt

The current scripts only support current LFRic trunk, i.e. they won't work with
LFRic 1.1 (due to missing directories in 1.1).

## Installing Fab build system into LFRic
This repository comes with a version of Fab as a submodule, to make sure the
scripts here have the matching Fab version available.

You need to have current trunk of PSyclone installed
(https://github.com/stfc/PSyclone). The API changes significantly in current trunk
(a 3.0 release is expected shortly), and the config
file included in LFRic and the example script relies on these new feature. This could
be changed to support both 2.5.0 and current trunk later.

### Installation

Check out this repository:

    git clone -b main  --recurse-submodules git@github.com:MetOffice/lfric-baf

If you already have cloned this repository without the `--recurse-submodules` option,
run:

    git submodule init
    git submodule update

to get Fab from the submodule.

Assuming that you prefer to use a python virtual environment, use the following:

     # Create a virtual environment and install psyclone
     cd lfric-baf
     python3 -m venv venv_fab
     source ./venv_fab/bin/activate
     # Install current PSyclone
     git clone https://github.com/stfc/PSyclone.git
     cd PSyclone
     pip3 install .

Install the included fab version:

     # Now install this fab:
     cd external/fab
     pip3 install .     # Without venv, use pip3 install --user .
     cd ../..

Then you need to copy the build system into the two LFRic repositories - core and apps.
Assuming that the two environment variable `LFRIC_CORE` and `LFRIC_APPS` point to the
checked out LFRic repositories, use:

     ./install.sh  $LFRIC_CORE $LFRIC_APPS

The script will do some simple tests to verify that the core and apps directory
indeed contain the expected LFRic repositories.

Fab-based build scripts will be installed into:

	- apps/applications/gravity_wave
	- apps/applications/gungho_model
	- apps/applications/lfric_atm
	- apps/applications/lfricinputs
	- core/applications/skeleton
	- core/mesh_tools


### Site-specific configuration

The fab build scripts will pickup site-specific configuration from directories under
`$LFRIC_CORE/infrastructure/build/fab/default`.

For now (until we have more changes implemented), it is recommended to copy
the whole directory `default` to a new subdirectory `YOURSITE_default`, e.g.
`nci_default` (which already exists). It is important that `_default` is added
(this is to support future setups that have different targets for one SITE, e.g.
meto_spice, meto_xc40, meto_xcs). Also make sure to use an underscore before
`default`, not a `minus` (since using a minus prevents python from importing
files from these subdirectories).
Then modify the file `setup_gnu.py` and if required add or modify linking options,
which are defined in the lines:

        linker.add_lib_flags("netcdf", nc_flibs, silent_replace=True)
        linker.add_lib_flags("yaxt", ["-lyaxt", "-lyaxt_c"])
        linker.add_lib_flags("xios", ["-lxios"])
        linker.add_lib_flags("hdf5", ["-lhdf5"])

The first parameter specifies the internal name for libraries, followed by a list
of linker options. If you should need additional library paths, you could e.g. use:

        linker.add_lib_flags("yaxt", ["-L", "/my/path/to/yaxt", "-lyaxt", "-lyaxt_c"])

It is important that each parameter (esp. `-L` etc) is an individual entry in the
list, otherwise they will not be properly recognised by the linker.

Similarly, you can change the compiler flags in the lines:

    gfortran = tr.get_tool(Category.FORTRAN_COMPILER, "gfortran")
    flags = ['-ffree-line-length-none', '-g',
             '-Werror=character-truncation', '-Werror=unused-value',
             '-Werror=tabs', '-fdefault-real-8', '-fdefault-double-8',
             '-Ditworks'
             ]
    gfortran.add_flags(flags)

### Building
In order to use the Fab build system, a wrapper script installed in the LFRic core
repository needs to be used. You need to start the build from the LFRic apps (or core)
repo (not from this repo). Example usage (but don't try this now):

    cd $LFRIC_APPS/applications/lfric_atm
    $LFRIC_CORE/build.sh ./fab_lfric_atm.py

The wrapper script `build.sh` makes sure that the build scripts installed into the
core repository will be found. Even if you are building an application in core,
you still need to invoke the `build.sh` script!

The new LFRic FAB build system relies on command line options to select compiler etc.
For building lfric_atm with gfortran (using mpif90 as a compiler wrapper that uses
gfortran), use:

    $LFRIC_CORE/build.sh ./fab_lfric_atm.py --site YOURSITE --suite gnu \
       -mpi -fc mpif90-gfortran -ld  linker-mpif90-gfortran

Note that the there is no `_default` added to the site, this will be added implicitly
by fab. This behaviour is meant for future improvements when the fab system will support 
different targets for one site. The options in detail:

- `--site` will make sure your modified config file is used to setup compiler options
- `--suite gnu` Makes the gnu compiler suite  and related compiler wrapper the default
- `-mpi` Enables MPI build
- `--fc mpif90-gfortran` Selects the Fortran compiler. Here mpif90 as compiler wrapper
  around gfortran will be used. If your mpif90 should not be using gfortran (e.g. 
  it might be using intel), this will be detected and the build will
  be aborted.
- `--ld linkfer-mpif90-gfortran` Specifies the linker.

It is not strictly necessary to specify the compiler and linker, selecting gnu as
compiler suite and specifying `-mpi` will be sufficient. But if your site installs
additional tools (e.g. we have profiling compiler wrappers), an unexpected compiler
or linker might be picked, hence it is recommended to be explicit.

The build directory will be under `$FAB_WORKSPACE`, with the name containing the application
and compiler, e.g. `lfric_atm-mpif90-gfortran`. If  `$FAB_WORKSPACE` is not defined, it
defaults to `$HOME/fab-workspace`. The build directory will contain the binary, all
original source files will be under `source`, and all files created during build (including
preprocessed files, PSyclone modified files, object files, ...) under `build_output`.

### Running PSyclone on UM files
This repository contains an additional script that shows how to use PSyclone to
additionally transform existing Fortran code using PSyclone's transformation ability
for the `LFRic_atm` apps. The script is called `./fab_lfric_atm_um_transform.py`.
It inherits the required source files from `./fab_lfric_atm.py` in the same directory,
and it is in turn based on `$LFRIC_CORE/infrastructure/build/fab/lfric_base.py` and
`baf_base.py` in the same directory. The two base classes in `LFRIC_CORE` provide
command line handling, running PSyclone on .x90 files etc. The application script
itself selects the requires source files and other repositories, and specifies
which libraries are required at link time. The example script 
`./fab_lfric_atm_um_transform.py` only contains the change required to add
an additional PSyclone step. It defines two methods:

- `psyclone`. This step overwrites the default PSyclone step. It first calls
  the original psyclone method (which processes all .x90 files). Then it
  loops over a list of files (with one file only specified as example),
  and calls psyclone for these files, creating a new output file with
  `_psyclonified` added to the file name. Then it replaces the original
  filename in the FORTRAN_BUILD_FILES artefact with the newly create file
  (with `psyclonified` added). Once this is done, the rest of the build
  system will then only compile the newly created file, the original file
  will not be compiled at all.
- `get_um_script` This method is passed to the psyclone process method, and
  it is used to determine which psyclone script is used to transform the
  specified file. In this example, it will always return
  `optimisation/umscript.py`. This script simple adds three comment lines
  at the top of the file.

Make sure to be in the LFRic applications repository with lfric_atm, then you
can build lfric_atm using

    cd $LFRIC_APPS/applications/lfric_atm
    $LFRIC_CORE/build.sh ./fab_lfric_atm_um_transform.py --site YOURSITE --suite gnu \
       -mpi -fc mpif90-gfortran -ld  linker-mpif90-gfortran

This will create a new directory under `FAB_WORKSPACE` called 
`lfric_atm_um_transform-mpif90-gfortran`. After the build process, you can check that
the file bdy_impl3 was transformed (some files have been removed in the output
below, so you will see more):

	~/fab-workspace/lfric_atm_um_transform-mpif90-gfortran$ find  . -iname bdy_impl3\*
	./source/science/um/atmosphere/boundary_layer/bdy_impl3.F90
	./build_output/science/um/atmosphere/boundary_layer/bdy_impl3.f90
	./build_output/science/um/atmosphere/boundary_layer/bdy_impl3_psyclonified.f90
	./build_output/bdy_impl3_mod.mod
	./build_output/_prebuild/bdy_impl3_psyclonified.59609a27b.o

The first line is the original input file. The next is the preprocessed file, which
is then processed by psyclone with the `umscript.py`. Then there is only one
.o file created, for the psyclonified file.

The two f90 files under build_output will be quite different (since PSyclone removes
comments and changes the layout), but at the top of the file you will see the lines:

	! Processed by umscript.py
	! ------------------------
	! 

The `umscript.py` explicitly adds these comments to each file it processes.
