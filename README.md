# LFRic-BAF

This repository contains the current state of BAF, the Build Architecture with
Fab. BAF is an object-oriented command line interface on top of the UK Met Office
build system Fab (https://github.com/MetOffice/fab). Fab itself is contained
as a submodule here, to ensure that the versions of BAF and FAB match.
It also contains LFRic-BAF, a complete new Fab-based build system for the
UK Met Office's LFRic simulation code, as an example of using BAF.

For now, you need to install this LFRic build system into existing LFRic repositories.
This way, building with Fab can be tested before the new Fab build system becomes
part of the LFRic repos. The documentation here describes how to install the
LFRic build scripts into existing LFRic repositories. This setup has been tested with
gfortran and ifort, this description assumes the usage of gfortran.

## Prerequisites
In order to use the build procedure below, you need to have:

- a Fortran compiler. For now supported are: `gfortran`, `ifort`,
`ifx`, Cray's `ftn`, `nvfortran`.
- `mpif90` as a compiler wrapper that calls your Fortran compiler.
- the correct rose-picker version (2.0.0)
- libclang and python-clang (dependencies of Fab)
- All lfric dependencies must be available, including:
  - netcdf (including the `nf-config` tool)
  - hdf5
  - xios, yaxt

  Installation of PSyclone and fparser is described below, you need at least
  PSyclone 3.0 and fparser 0.2, older versions will result in build failures.

For the documentation, you need to additionally install:
- sphinx
- sphinx_design (??)
- sphinx-autodoc-typehints (??)
- autoapi (??)


The build scripts support current LFRic trunk. Depending on LFRic version,
additional directories might need to be listed or be removed.

### Installation

Check out this repository:

    git clone --recurse-submodules git@github.com:MetOffice/lfric-baf

If you already have cloned this repository without the `--recurse-submodules` option,
run:

    git submodule init
    git submodule update

to get Fab from the submodule.

You need to have current trunk of PSyclone installed
(https://github.com/stfc/PSyclone). The API changes significantly in current trunk
(a 3.0 release is expected shortly), and the config
file included in LFRic and the example script relies on these new feature. 

If required, install current PSyclone in a Python virtual environment:

     # Create a virtual environment and install psyclone
     cd lfric-baf
     python3 -m venv venv_fab
     source ./venv_fab/bin/activate
     # Install current PSyclone
     git clone https://github.com/stfc/PSyclone.git
     cd PSyclone
     pip3 install .
     cd ..

Note that this will also install the right version of fparser. This build system
will only work with fparser 0.2 (or later).

Install the fab version included in lfric-baf:

     # Now install this fab:
     cd fab
     pip3 install .     # Without venv, use pip3 install --user .
     cd ..

Then you need to copy the build system into the two LFRic repositories - core and apps.
Assuming that the two environment variable `LFRIC_CORE` and `LFRIC_APPS` point to the
checked-out LFRic repositories, use:

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

For now, it is recommended to copy the `niwa_xc50` directory, which shows how
to implement a (initially) empty site-specific setup. It will inherit all
functionality from the default configuration directory, which will setup
sensible defaults for all supported compilers. Use a two-part name,
the first part identifying your site, the second part the platform you are using.
If you have only one site, use `default` as platform (which is the default
used by Baf). Make sure to use an underscore between site and platform, not a
`minus` (since using a minus prevents Python from importing
files from these subdirectories, which can be useful).

The `niwa_xc50/config.py` file shows how to modify the linker options
as a simple example.


### Building
In order to use the Fab build system, a wrapper script installed in the LFRic core
repository needs to be used. You need to start the build from the LFRic apps (or core)
repo (not from this repo). Example usage (but don't try this now):

    cd $LFRIC_APPS/applications/lfric_atm
    $LFRIC_CORE/build.sh ./fab_lfric_atm.py

The wrapper script `build.sh` makes sure that the build scripts installed into the
core repository will be found. Even if you are building an application in core,
you still need to invoke the `build.sh` script to allow BAF to setup the Python
import infrastructure!

The new LFRic FAB build system relies on command line options to select compiler etc.
For building lfric_atm with gfortran (using mpif90 as a compiler wrapper that uses
gfortran), use:

    $LFRIC_CORE/build.sh ./fab_lfric_atm.py --site YOURSITE --platform YOUR_PLATFORM \
       --suite gnu \
       -mpi -fc mpif90-gfortran -ld  linker-mpif90-gfortran

If you have only one platform and therefore use `default` as name, there is no need
to specify the `--platform` command line options, it will default to `default`.

The options in detail:

- `--site` will make sure your modified config file is used to setup compiler options
- `--suite gnu` makes the gnu compiler suite  and related compiler wrapper the default.
- `-mpi` Enables MPI build
- `--fc mpif90-gfortran` selects the Fortran compiler. Here mpif90 as compiler wrapper
  around gfortran will be used. If your mpif90 should not be using gfortran (e.g. 
  it might be using intel), this will be detected and the build will
  be aborted. It might not be necessary to specify the compiler explicitly,
  since the default suite and the fact that MPI is enabled should allow Fab to
  detect this automatically. But it can be required if different compilers and
  compiler wrappers are available that would all fulfil the requirements.
- `--ld linkfer-mpif90-gfortran` specifies the linker. This is for now required
  to ensure that a Fortran compiler is used for linking, since Fab does not know
  if linking should be done with C or Fortran (e.g. mpicc or mpif90), and it might
  pick the wrong one. The name of a linker always starts with `linker-`, followed
  by the name of the compiler to use.

It is not strictly necessary to specify the compiler, selecting gnu as
compiler suite and specifying `-mpi` will be sufficient. But if your site installs
additional tools (e.g. we have profiling compiler wrappers), an unexpected compiler
or linker might be picked, hence it is recommended to be explicit.

If you have problems with the compiler names, run a build script with the option
`--available-compilers`, which will list all available compiler and linkers, and also
include debug output why other compilers were not marked as available.

Example output:

    ----- Available compiler and linkers -----
    Gcc - gcc: gcc
    Mpicc(gcc)
    Gfortran - gfortran: gfortran
    Mpif90(gfortran)
    Linker - linker-gcc: gcc
    Linker - linker-gfortran: gfortran
    Linker - linker-mpif90-gfortran: mpif90
    Linker - linker-mpicc-gcc: mpicc


The build directory will be under `$FAB_WORKSPACE`, with the name containing the application
and compiler, e.g. `lfric_atm-mpif90-gfortran`. If `$FAB_WORKSPACE` is not defined, it
defaults to `$HOME/fab-workspace`. The build directory will contain the binary, all
original source files will be under `source`, and all files created during build (including
preprocessed files, PSyclone modified files, object files, ...) under `build_output`.

### Usage on Cray systems
On Cray XCs, the recommended way of building code is to use the Cray-supplied
compiler wrappers (e.g. `ftn`). FAB supports these wrappers, but it will be required
to explicitly specify the compilers to use (since FAB will otherwise detect e.g. 
`ifort`, instead of using `ftn` as wrapper around `ifort`). Since Crays also use
`cc` as wrapper, which can lead to confusion on non-cray systems, these wrappers
are named `crayftn` and `craycc`. Use the following to select the right compiler:
- `crayftn-ftn` - Use the CCE compilers
- `crayftn-ifort` - Use `ftn` with Intel's `ifort`
- `crayftn-gfortran` - Use `ftn` with GNU's `gfortran`.
- `craycc-cc` - Use the CCE compilers
- `craycc-icc` - Use `cc` with Intel's `icc`
- `craycc-gcc` - Use `cc` with GNU's `gcc`
- `linker-crayftn-ifort` - Use the Cray `ftn` wrapper for `ifort` as linker.
   Etc. for other linkers.

Example usage using Cray's CCE (assuming that `core` is next to `apps`:

    cd apps/applications/gungho
    ../../../core/build.sh ./fab_gungho.py -fc crayftn-ftn -ld linker-crayftn-ftn


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
