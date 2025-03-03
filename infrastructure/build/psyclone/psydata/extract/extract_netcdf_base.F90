! ================================================== !
! THIS FILE IS CREATED FROM THE JINJA TEMPLATE FILE. !
! DO NOT MODIFY DIRECTLY!                            !
! ================================================== !



! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2020-2025, Science and Technology Facilities Council.
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
! "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
! LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
! FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
! COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
! INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
! BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
! LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
! LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
! ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
! Author: J. Henrichs, Bureau of Meteorology
! Modified: I. Kavcic, Met Office

!> This module implements a simple NetCDF writer using the PSyData
!! interface. A Fortran code instrumented with corresponding calls
!! to the PSyData API and linked in with this library will create
!! a NetCDF file that contains all scalar values, and the dimensions
!! and content for each array.

module extract_netcdf_base_mod

    use psy_data_base_mod, only : PSyDataBaseType, is_enabled

    use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                              real32, real64, &
                                              stderr => Error_Unit

    implicit none

    !> This is the data type that manages the information required
    !! to write data to a NetCDF file using the PSyData API. A
    !! static instance of this type is created for each instrumented
    !! region with PSyclone (and each region will write a separate
    !! file).
    type, extends(PSyDataBaseType), public :: ExtractNetcdfBaseType

        !> The NetCDF ID used for this file.
        integer                            :: ncid
        !> Each variable ID. This is required to associate data
        !! with the declared variables: the variables are declared
        !! in the same order in which their value is provided

        integer, dimension(:), allocatable :: var_id

    contains

        ! The various procedures used
        procedure :: PreStart
        procedure :: PreEndDeclaration
        procedure :: PostEnd

        procedure :: DeclareScalarChar
        procedure :: WriteScalarChar
        procedure :: DeclareArray1dChar
        procedure :: WriteArray1dChar
        procedure :: DeclareArray2dChar
        procedure :: WriteArray2dChar
        procedure :: DeclareArray3dChar
        procedure :: WriteArray3dChar
        procedure :: DeclareArray4dChar
        procedure :: WriteArray4dChar
        procedure :: DeclareScalarInt
        procedure :: WriteScalarInt
        procedure :: DeclareArray1dInt
        procedure :: WriteArray1dInt
        procedure :: DeclareArray2dInt
        procedure :: WriteArray2dInt
        procedure :: DeclareArray3dInt
        procedure :: WriteArray3dInt
        procedure :: DeclareArray4dInt
        procedure :: WriteArray4dInt
        procedure :: DeclareScalarLong
        procedure :: WriteScalarLong
        procedure :: DeclareArray1dLong
        procedure :: WriteArray1dLong
        procedure :: DeclareArray2dLong
        procedure :: WriteArray2dLong
        procedure :: DeclareArray3dLong
        procedure :: WriteArray3dLong
        procedure :: DeclareArray4dLong
        procedure :: WriteArray4dLong
        procedure :: DeclareScalarLogical
        procedure :: WriteScalarLogical
        procedure :: DeclareArray1dLogical
        procedure :: WriteArray1dLogical
        procedure :: DeclareArray2dLogical
        procedure :: WriteArray2dLogical
        procedure :: DeclareArray3dLogical
        procedure :: WriteArray3dLogical
        procedure :: DeclareArray4dLogical
        procedure :: WriteArray4dLogical
        procedure :: DeclareScalarReal
        procedure :: WriteScalarReal
        procedure :: DeclareArray1dReal
        procedure :: WriteArray1dReal
        procedure :: DeclareArray2dReal
        procedure :: WriteArray2dReal
        procedure :: DeclareArray3dReal
        procedure :: WriteArray3dReal
        procedure :: DeclareArray4dReal
        procedure :: WriteArray4dReal
        procedure :: DeclareScalarDouble
        procedure :: WriteScalarDouble
        procedure :: DeclareArray1dDouble
        procedure :: WriteArray1dDouble
        procedure :: DeclareArray2dDouble
        procedure :: WriteArray2dDouble
        procedure :: DeclareArray3dDouble
        procedure :: WriteArray3dDouble
        procedure :: DeclareArray4dDouble
        procedure :: WriteArray4dDouble

        ! Declare generic interface for PreDeclareVariable:
        generic, public :: PreDeclareVariable => &
            DeclareScalarChar, &
            DeclareArray1dChar, &
            DeclareArray2dChar, &
            DeclareArray3dChar, &
            DeclareArray4dChar, &
            DeclareScalarInt, &
            DeclareArray1dInt, &
            DeclareArray2dInt, &
            DeclareArray3dInt, &
            DeclareArray4dInt, &
            DeclareScalarLong, &
            DeclareArray1dLong, &
            DeclareArray2dLong, &
            DeclareArray3dLong, &
            DeclareArray4dLong, &
            DeclareScalarLogical, &
            DeclareArray1dLogical, &
            DeclareArray2dLogical, &
            DeclareArray3dLogical, &
            DeclareArray4dLogical, &
            DeclareScalarReal, &
            DeclareArray1dReal, &
            DeclareArray2dReal, &
            DeclareArray3dReal, &
            DeclareArray4dReal, &
            DeclareScalarDouble, &
            DeclareArray1dDouble, &
            DeclareArray2dDouble, &
            DeclareArray3dDouble, &
            DeclareArray4dDouble

        !> The generic interface for providing the value of variables:
        generic, public :: ProvideVariable => &
            WriteScalarChar, &
            WriteArray1dChar, &
            WriteArray2dChar, &
            WriteArray3dChar, &
            WriteArray4dChar, &
            WriteScalarInt, &
            WriteArray1dInt, &
            WriteArray2dInt, &
            WriteArray3dInt, &
            WriteArray4dInt, &
            WriteScalarLong, &
            WriteArray1dLong, &
            WriteArray2dLong, &
            WriteArray3dLong, &
            WriteArray4dLong, &
            WriteScalarLogical, &
            WriteArray1dLogical, &
            WriteArray2dLogical, &
            WriteArray3dLogical, &
            WriteArray4dLogical, &
            WriteScalarReal, &
            WriteArray1dReal, &
            WriteArray2dReal, &
            WriteArray3dReal, &
            WriteArray4dReal, &
            WriteScalarDouble, &
            WriteArray1dDouble, &
            WriteArray2dDouble, &
            WriteArray3dDouble, &
            WriteArray4dDouble

    end type ExtractNetcdfBaseType

contains

    ! -------------------------------------------------------------------------
    !> @brief Checks if the return value from a NetCDF call indicates an error.
    !! If so, print the corresponding error message and aborts the program.
    !! It is typically used as a wrapper around NetCDF calls:
    !! retval = CheckError(nf90_close(ncid))
    !! @param[in] retval The return value from a NetCDF operation.
    !! Returns the return value.
    function CheckError(retval)

        use netcdf, only : nf90_noerr, nf90_strerror

        implicit none

        integer, intent(in) :: retval
        integer             :: CheckError

        if (retval /= nf90_noerr) then
            write(stderr, *) "NetCDF Error:"
            write(stderr, *) trim(nf90_strerror(retval))
            stop
        endif
        CheckError = retval

    end function CheckError

    ! -------------------------------------------------------------------------
    !> @brief This is a one-time init function. It is not required for the kernel
    !! extraction and is therefore empty.
    subroutine extract_PSyDataInit()
        implicit none
    end subroutine extract_PSyDataInit

    ! -------------------------------------------------------------------------
    !> @brief This is a one-time shutdown function. It is not required for the kernel
    !! extraction and is therefore empty.
    subroutine extract_PSyDataShutdown()
        implicit none
    end subroutine extract_PSyDataShutdown

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is the first function called when data is written out
    !! before an instrumented region of code.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] module_name The name of the module of the instrumented
    !!            region.
    !! @param[in] region_name The name of the instrumented region.
    !! @param[in] num_pre_vars The number of variables that are declared and
    !!            written before the instrumented region.
    !! @param[in] num_post_vars The number of variables that are also declared
    !!            before an instrumented region of code, but are written after
    !!            this region.
    subroutine PreStart(this, module_name, region_name, num_pre_vars, &
                        num_post_vars)

#ifndef NO_MPI
        use mpi
#endif
        use netcdf, only : nf90_create, NF90_CLOBBER, NF90_NETCDF4

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: module_name, &
                                                               region_name
        integer, intent(in)                                 :: num_pre_vars, &
                                                               num_post_vars

        integer :: retval
        character(1024) :: file_name
#ifndef NO_MPI
        integer :: rank, size, ierr, num_digits
        character(7) :: rank_format, rank_string
#endif

        call this%PSyDataBaseType%PreStart(module_name, region_name, &
                                           num_pre_vars, num_post_vars)
        if (this%verbosity >= 1) then
            write(stderr,*) "Opening ", trim(module_name) // "-" // &
                            trim(region_name) // ".nc"
        endif


#ifdef NO_MPI
        file_name = module_name//"-"//region_name//".nc"
#else
        ! Add the rank to the file name:
        call MPI_Comm_size(MPI_COMM_WORLD, size, ierr)
        call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
        num_digits = floor(log(real(size))/log(10.0)) + 1
        write(rank_format, "('(I',I0,'.',I0,')')") num_digits, num_digits
        write(rank_string, rank_format) rank
        file_name = module_name//"-"//region_name//"-"//trim(rank_string)//".nc"
#endif

        ! Open the NetCDF file. Explicitly request NetCDF 4 format, since
        ! this is required in order to use NF90_INT64 (further down)
        retval = CheckError(nf90_create(trim(file_name), &
                                        IOR(NF90_NETCDF4,NF90_CLOBBER),       &
                                        this%ncid))

        ! Allocate the array that will store the variable IDs of all
        ! variables that are going to be declared. Note that there might
        ! actually be more variables stored (in LFRic vector fields are
        ! stored as individual NetCDF variables, so a 3d vector field
        ! would actually use 3 individual NetCDF variables). If required,
        ! this array will be re-allocated in the declare functions.
        if (.not. allocated(this%var_id)) then
            allocate(this%var_id(num_pre_vars+num_post_vars))
        endif

    end subroutine PreStart

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called once all variables are declared (this includes
    !! variables that will be written before as well as variables that are
    !! written after the instrumented region). It is used to switch the NetCDF
    !! file from declaration to writing state, and reset the next_var_index
    !! back to 1.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    subroutine PreEndDeclaration(this)

        use netcdf, only : nf90_enddef

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this

        integer :: retval

        call this%PSyDataBaseType%PreEndDeclaration()
        if (this%verbosity >= 1) then
            write(stderr,*) "Ending definition ", trim(this%module_name) // &
                            "-"//trim(this%region_name)//".nc"
        endif
        retval = CheckError(nf90_enddef(this%ncid))

    end subroutine PreEndDeclaration

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called after the instrumented region has been
    !! executed and all values of variables after the instrumented
    !! region have been provided. This will close the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    subroutine PostEnd(this)

        use netcdf, only : nf90_close

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this

        integer :: retval
        if (this%verbosity >= 1) then
            write(stderr,*) "Closing ", trim(this%module_name) // "-" // &
                            trim(this%region_name) // ".nc"
        endif
        retval = CheckError(nf90_close(this%ncid))
        call this%PSyDataBaseType%PostEnd()

    end subroutine PostEnd

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar character(*) value.
    !! A corresponding variable definition is added to the NetCDF file, and
    !! the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarChar(this, name, value)

        use netcdf, only : nf90_def_var, NF90_CHAR

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), intent(in)                                :: value

        integer                            :: retval
        integer, dimension(:), allocatable :: tmp_var_id

        if (this%next_var_index > size(this%var_id)) then
            ! This can happen in LFRic when vector fields are used
            ! Each dimension of this vector becomes one NetCDF
            ! variable, so we need to potentially reallocate this field
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif
        if (this%verbosity >= 2) then
            write(stderr,*) "Defining Char."
        endif
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_CHAR, &
                                         this%var_id(this%next_var_index)))
        call this%PSyDataBaseType%DeclareScalarChar(name, value)

    end subroutine DeclareScalarChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes the value of a scalar character(*)
    !! variable to the NetCDF file. It takes the variable id from the
    !! corresponding declaration.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteScalarChar(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), intent(in)                                :: value
        integer                                             :: retval
if (this%verbosity >= 2) then
            write(stderr,*) "Writing Char."
        endif
retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value))
call this%PSyDataBaseType%ProvideScalarChar(name, value)

    end subroutine WriteScalarChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 1D array of character(*).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dChar(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:), intent(in)      :: value

        integer                            :: dimid1
        integer                            :: retval
        integer, dimension(1)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Char."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        dimids =  (/ dimid1 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_CHAR, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray1dChar(name, value)

    end subroutine DeclareArray1dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 1D array of character(*)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray1dChar(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Char."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:)))
        call this%PSyDataBaseType%ProvideArray1dChar(name, value)

    end subroutine WriteArray1dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 2D array of character(*).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dChar(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2
        integer                            :: retval
        integer, dimension(2)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Char."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        dimids =  (/ dimid1, dimid2 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_CHAR, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray2dChar(name, value)

    end subroutine DeclareArray2dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 2D array of character(*)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray2dChar(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Char."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:)))
        call this%PSyDataBaseType%ProvideArray2dChar(name, value)

    end subroutine WriteArray2dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 3D array of character(*).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dChar(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3
        integer                            :: retval
        integer, dimension(3)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Char."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        dimids =  (/ dimid1, dimid2, dimid3 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_CHAR, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray3dChar(name, value)

    end subroutine DeclareArray3dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 3D array of character(*)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray3dChar(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Char."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:)))
        call this%PSyDataBaseType%ProvideArray3dChar(name, value)

    end subroutine WriteArray3dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 4D array of character(*).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dChar(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:,:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3, dimid4
        integer                            :: retval
        integer, dimension(4)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Char."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%4", &
                                         size(value,4), dimid4))
        dimids =  (/ dimid1, dimid2, dimid3, dimid4 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_CHAR, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray4dChar(name, value)

    end subroutine DeclareArray4dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 4D array of character(*)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray4dChar(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        character(*), dimension(:,:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Char."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:,:)))
        call this%PSyDataBaseType%ProvideArray4dChar(name, value)

    end subroutine WriteArray4dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar integer(kind=int32) value.
    !! A corresponding variable definition is added to the NetCDF file, and
    !! the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarInt(this, name, value)

        use netcdf, only : nf90_def_var, NF90_INT

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), intent(in)                                :: value

        integer                            :: retval
        integer, dimension(:), allocatable :: tmp_var_id

        if (this%next_var_index > size(this%var_id)) then
            ! This can happen in LFRic when vector fields are used
            ! Each dimension of this vector becomes one NetCDF
            ! variable, so we need to potentially reallocate this field
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif
        if (this%verbosity >= 2) then
            write(stderr,*) "Defining Int."
        endif
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         this%var_id(this%next_var_index)))
        call this%PSyDataBaseType%DeclareScalarInt(name, value)

    end subroutine DeclareScalarInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes the value of a scalar integer(kind=int32)
    !! variable to the NetCDF file. It takes the variable id from the
    !! corresponding declaration.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteScalarInt(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), intent(in)                                :: value
        integer                                             :: retval
if (this%verbosity >= 2) then
            write(stderr,*) "Writing Int."
        endif
retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value))
call this%PSyDataBaseType%ProvideScalarInt(name, value)

    end subroutine WriteScalarInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 1D array of integer(kind=int32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dInt(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:), intent(in)      :: value

        integer                            :: dimid1
        integer                            :: retval
        integer, dimension(1)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Int."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        dimids =  (/ dimid1 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray1dInt(name, value)

    end subroutine DeclareArray1dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 1D array of integer(kind=int32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray1dInt(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Int."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:)))
        call this%PSyDataBaseType%ProvideArray1dInt(name, value)

    end subroutine WriteArray1dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 2D array of integer(kind=int32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dInt(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2
        integer                            :: retval
        integer, dimension(2)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Int."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        dimids =  (/ dimid1, dimid2 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray2dInt(name, value)

    end subroutine DeclareArray2dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 2D array of integer(kind=int32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray2dInt(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Int."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:)))
        call this%PSyDataBaseType%ProvideArray2dInt(name, value)

    end subroutine WriteArray2dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 3D array of integer(kind=int32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dInt(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3
        integer                            :: retval
        integer, dimension(3)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Int."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        dimids =  (/ dimid1, dimid2, dimid3 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray3dInt(name, value)

    end subroutine DeclareArray3dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 3D array of integer(kind=int32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray3dInt(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Int."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:)))
        call this%PSyDataBaseType%ProvideArray3dInt(name, value)

    end subroutine WriteArray3dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 4D array of integer(kind=int32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dInt(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:,:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3, dimid4
        integer                            :: retval
        integer, dimension(4)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Int."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%4", &
                                         size(value,4), dimid4))
        dimids =  (/ dimid1, dimid2, dimid3, dimid4 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray4dInt(name, value)

    end subroutine DeclareArray4dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 4D array of integer(kind=int32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray4dInt(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int32), dimension(:,:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Int."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:,:)))
        call this%PSyDataBaseType%ProvideArray4dInt(name, value)

    end subroutine WriteArray4dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar integer(kind=int64) value.
    !! A corresponding variable definition is added to the NetCDF file, and
    !! the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarLong(this, name, value)

        use netcdf, only : nf90_def_var, NF90_INT64

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), intent(in)                                :: value

        integer                            :: retval
        integer, dimension(:), allocatable :: tmp_var_id

        if (this%next_var_index > size(this%var_id)) then
            ! This can happen in LFRic when vector fields are used
            ! Each dimension of this vector becomes one NetCDF
            ! variable, so we need to potentially reallocate this field
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif
        if (this%verbosity >= 2) then
            write(stderr,*) "Defining Long."
        endif
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT64, &
                                         this%var_id(this%next_var_index)))
        call this%PSyDataBaseType%DeclareScalarLong(name, value)

    end subroutine DeclareScalarLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes the value of a scalar integer(kind=int64)
    !! variable to the NetCDF file. It takes the variable id from the
    !! corresponding declaration.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteScalarLong(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), intent(in)                                :: value
        integer                                             :: retval
if (this%verbosity >= 2) then
            write(stderr,*) "Writing Long."
        endif
retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value))
call this%PSyDataBaseType%ProvideScalarLong(name, value)

    end subroutine WriteScalarLong



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 1D array of integer(kind=int64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dLong(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:), intent(in)      :: value

        integer                            :: dimid1
        integer                            :: retval
        integer, dimension(1)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Long."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        dimids =  (/ dimid1 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT64, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray1dLong(name, value)

    end subroutine DeclareArray1dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 1D array of integer(kind=int64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray1dLong(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Long."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:)))
        call this%PSyDataBaseType%ProvideArray1dLong(name, value)

    end subroutine WriteArray1dLong



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 2D array of integer(kind=int64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dLong(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2
        integer                            :: retval
        integer, dimension(2)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Long."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        dimids =  (/ dimid1, dimid2 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT64, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray2dLong(name, value)

    end subroutine DeclareArray2dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 2D array of integer(kind=int64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray2dLong(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Long."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:)))
        call this%PSyDataBaseType%ProvideArray2dLong(name, value)

    end subroutine WriteArray2dLong



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 3D array of integer(kind=int64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dLong(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3
        integer                            :: retval
        integer, dimension(3)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Long."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        dimids =  (/ dimid1, dimid2, dimid3 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT64, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray3dLong(name, value)

    end subroutine DeclareArray3dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 3D array of integer(kind=int64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray3dLong(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Long."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:)))
        call this%PSyDataBaseType%ProvideArray3dLong(name, value)

    end subroutine WriteArray3dLong



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 4D array of integer(kind=int64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dLong(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:,:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3, dimid4
        integer                            :: retval
        integer, dimension(4)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Long."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%4", &
                                         size(value,4), dimid4))
        dimids =  (/ dimid1, dimid2, dimid3, dimid4 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT64, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray4dLong(name, value)

    end subroutine DeclareArray4dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 4D array of integer(kind=int64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray4dLong(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        integer(kind=int64), dimension(:,:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Long."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:,:)))
        call this%PSyDataBaseType%ProvideArray4dLong(name, value)

    end subroutine WriteArray4dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar Logical(kind=4) value.
    !! A corresponding variable definition is added to the NetCDF file, and
    !! the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarLogical(this, name, value)

        use netcdf, only : nf90_def_var, NF90_INT

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), intent(in)                                :: value

        integer                            :: retval
        integer, dimension(:), allocatable :: tmp_var_id

        if (this%next_var_index > size(this%var_id)) then
            ! This can happen in LFRic when vector fields are used
            ! Each dimension of this vector becomes one NetCDF
            ! variable, so we need to potentially reallocate this field
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif
        if (this%verbosity >= 2) then
            write(stderr,*) "Defining Logical."
        endif
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         this%var_id(this%next_var_index)))
        call this%PSyDataBaseType%DeclareScalarLogical(name, value)

    end subroutine DeclareScalarLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes the value of a scalar Logical(kind=4)
    !! variable to the NetCDF file. It takes the variable id from the
    !! corresponding declaration.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteScalarLogical(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), intent(in)                                :: value
        integer                                             :: retval
        integer                                             :: tmp
if (this%verbosity >= 2) then
            write(stderr,*) "Writing Logical."
        endif
        if (value) then
            tmp = 1
        else
            tmp = 0
        endif
        retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         tmp))
call this%PSyDataBaseType%ProvideScalarLogical(name, value)

    end subroutine WriteScalarLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 1D array of Logical(kind=4).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dLogical(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:), intent(in)      :: value

        integer                            :: dimid1
        integer                            :: retval
        integer, dimension(1)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Logical."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        dimids =  (/ dimid1 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray1dLogical(name, value)

    end subroutine DeclareArray1dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 1D array of Logical(kind=4)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray1dLogical(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:), intent(in)      :: value

        integer :: retval
        integer, dimension(size(value,1)) :: tmp

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Logical."
        endif

        where(value)
            tmp = 1
        elsewhere
            tmp = 0
        endwhere
        retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         tmp(:)))
        call this%PSyDataBaseType%ProvideArray1dLogical(name, value)

    end subroutine WriteArray1dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 2D array of Logical(kind=4).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dLogical(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2
        integer                            :: retval
        integer, dimension(2)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Logical."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        dimids =  (/ dimid1, dimid2 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray2dLogical(name, value)

    end subroutine DeclareArray2dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 2D array of Logical(kind=4)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray2dLogical(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:,:), intent(in)      :: value

        integer :: retval
        integer, dimension(size(value,1), size(value,2)) :: tmp

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Logical."
        endif

        where(value)
            tmp = 1
        elsewhere
            tmp = 0
        endwhere
        retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         tmp(:,:)))
        call this%PSyDataBaseType%ProvideArray2dLogical(name, value)

    end subroutine WriteArray2dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 3D array of Logical(kind=4).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dLogical(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3
        integer                            :: retval
        integer, dimension(3)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Logical."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        dimids =  (/ dimid1, dimid2, dimid3 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray3dLogical(name, value)

    end subroutine DeclareArray3dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 3D array of Logical(kind=4)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray3dLogical(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:,:,:), intent(in)      :: value

        integer :: retval
        integer, dimension(size(value,1), size(value,2), size(value,3)) :: tmp

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Logical."
        endif

        where(value)
            tmp = 1
        elsewhere
            tmp = 0
        endwhere
        retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         tmp(:,:,:)))
        call this%PSyDataBaseType%ProvideArray3dLogical(name, value)

    end subroutine WriteArray3dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 4D array of Logical(kind=4).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dLogical(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:,:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3, dimid4
        integer                            :: retval
        integer, dimension(4)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Logical."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%4", &
                                         size(value,4), dimid4))
        dimids =  (/ dimid1, dimid2, dimid3, dimid4 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_INT, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray4dLogical(name, value)

    end subroutine DeclareArray4dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 4D array of Logical(kind=4)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray4dLogical(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        Logical(kind=4), dimension(:,:,:,:), intent(in)      :: value

        integer :: retval
        integer, dimension(size(value,1), size(value,2), size(value,3), size(value,4)) :: tmp

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Logical."
        endif

        where(value)
            tmp = 1
        elsewhere
            tmp = 0
        endwhere
        retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         tmp(:,:,:,:)))
        call this%PSyDataBaseType%ProvideArray4dLogical(name, value)

    end subroutine WriteArray4dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar real(kind=real32) value.
    !! A corresponding variable definition is added to the NetCDF file, and
    !! the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarReal(this, name, value)

        use netcdf, only : nf90_def_var, NF90_REAL

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), intent(in)                                :: value

        integer                            :: retval
        integer, dimension(:), allocatable :: tmp_var_id

        if (this%next_var_index > size(this%var_id)) then
            ! This can happen in LFRic when vector fields are used
            ! Each dimension of this vector becomes one NetCDF
            ! variable, so we need to potentially reallocate this field
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif
        if (this%verbosity >= 2) then
            write(stderr,*) "Defining Real."
        endif
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_REAL, &
                                         this%var_id(this%next_var_index)))
        call this%PSyDataBaseType%DeclareScalarReal(name, value)

    end subroutine DeclareScalarReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes the value of a scalar real(kind=real32)
    !! variable to the NetCDF file. It takes the variable id from the
    !! corresponding declaration.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteScalarReal(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), intent(in)                                :: value
        integer                                             :: retval
if (this%verbosity >= 2) then
            write(stderr,*) "Writing Real."
        endif
retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value))
call this%PSyDataBaseType%ProvideScalarReal(name, value)

    end subroutine WriteScalarReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 1D array of real(kind=real32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dReal(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:), intent(in)      :: value

        integer                            :: dimid1
        integer                            :: retval
        integer, dimension(1)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Real."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        dimids =  (/ dimid1 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_REAL, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray1dReal(name, value)

    end subroutine DeclareArray1dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 1D array of real(kind=real32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray1dReal(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Real."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:)))
        call this%PSyDataBaseType%ProvideArray1dReal(name, value)

    end subroutine WriteArray1dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 2D array of real(kind=real32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dReal(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2
        integer                            :: retval
        integer, dimension(2)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Real."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        dimids =  (/ dimid1, dimid2 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_REAL, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray2dReal(name, value)

    end subroutine DeclareArray2dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 2D array of real(kind=real32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray2dReal(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Real."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:)))
        call this%PSyDataBaseType%ProvideArray2dReal(name, value)

    end subroutine WriteArray2dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 3D array of real(kind=real32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dReal(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3
        integer                            :: retval
        integer, dimension(3)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Real."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        dimids =  (/ dimid1, dimid2, dimid3 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_REAL, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray3dReal(name, value)

    end subroutine DeclareArray3dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 3D array of real(kind=real32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray3dReal(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Real."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:)))
        call this%PSyDataBaseType%ProvideArray3dReal(name, value)

    end subroutine WriteArray3dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 4D array of real(kind=real32).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dReal(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:,:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3, dimid4
        integer                            :: retval
        integer, dimension(4)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Real."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%4", &
                                         size(value,4), dimid4))
        dimids =  (/ dimid1, dimid2, dimid3, dimid4 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_REAL, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray4dReal(name, value)

    end subroutine DeclareArray4dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 4D array of real(kind=real32)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray4dReal(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real32), dimension(:,:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Real."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:,:)))
        call this%PSyDataBaseType%ProvideArray4dReal(name, value)

    end subroutine WriteArray4dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar real(kind=real64) value.
    !! A corresponding variable definition is added to the NetCDF file, and
    !! the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarDouble(this, name, value)

        use netcdf, only : nf90_def_var, NF90_DOUBLE

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), intent(in)                                :: value

        integer                            :: retval
        integer, dimension(:), allocatable :: tmp_var_id

        if (this%next_var_index > size(this%var_id)) then
            ! This can happen in LFRic when vector fields are used
            ! Each dimension of this vector becomes one NetCDF
            ! variable, so we need to potentially reallocate this field
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif
        if (this%verbosity >= 2) then
            write(stderr,*) "Defining Double."
        endif
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_DOUBLE, &
                                         this%var_id(this%next_var_index)))
        call this%PSyDataBaseType%DeclareScalarDouble(name, value)

    end subroutine DeclareScalarDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes the value of a scalar real(kind=real64)
    !! variable to the NetCDF file. It takes the variable id from the
    !! corresponding declaration.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteScalarDouble(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), intent(in)                                :: value
        integer                                             :: retval
if (this%verbosity >= 2) then
            write(stderr,*) "Writing Double."
        endif
retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value))
call this%PSyDataBaseType%ProvideScalarDouble(name, value)

    end subroutine WriteScalarDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 1D array of real(kind=real64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dDouble(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:), intent(in)      :: value

        integer                            :: dimid1
        integer                            :: retval
        integer, dimension(1)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Double."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        dimids =  (/ dimid1 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_DOUBLE, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray1dDouble(name, value)

    end subroutine DeclareArray1dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 1D array of real(kind=real64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray1dDouble(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Double."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:)))
        call this%PSyDataBaseType%ProvideArray1dDouble(name, value)

    end subroutine WriteArray1dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 2D array of real(kind=real64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dDouble(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2
        integer                            :: retval
        integer, dimension(2)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Double."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        dimids =  (/ dimid1, dimid2 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_DOUBLE, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray2dDouble(name, value)

    end subroutine DeclareArray2dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 2D array of real(kind=real64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray2dDouble(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Double."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:)))
        call this%PSyDataBaseType%ProvideArray2dDouble(name, value)

    end subroutine WriteArray2dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 3D array of real(kind=real64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dDouble(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3
        integer                            :: retval
        integer, dimension(3)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Double."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        dimids =  (/ dimid1, dimid2, dimid3 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_DOUBLE, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray3dDouble(name, value)

    end subroutine DeclareArray3dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 3D array of real(kind=real64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray3dDouble(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Double."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:)))
        call this%PSyDataBaseType%ProvideArray3dDouble(name, value)

    end subroutine WriteArray3dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a 4D array of real(kind=real64).
    !! A corresponding variable and dimension definitions are added
    !! to the NetCDF file, and the variable id is stored in the var_id field.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dDouble(this, name, value)

        use netcdf

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:,:,:,:), intent(in)      :: value

        integer                            :: dimid1, dimid2, dimid3, dimid4
        integer                            :: retval
        integer, dimension(4)        :: dimids
        integer, dimension(:), allocatable :: tmp_var_id

        if (.not. is_enabled) return

        if (this%next_var_index > size(this%var_id)) then
            allocate(tmp_var_id(2*size(this%var_id)))
            tmp_var_id(1:size(this%var_id)) = this%var_id
            deallocate(this%var_id)
            call move_alloc(tmp_var_id, this%var_id)
            ! tmp_var_id is deallocated as part of move_alloc
        endif

        if (this%verbosity >= 2) then
            write(stderr,*) "Declaring Array Double."
        endif
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%1", &
                                         size(value,1), dimid1))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%2", &
                                         size(value,2), dimid2))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%3", &
                                         size(value,3), dimid3))
        ! A '%' is added to avoid a clash if the user should have say
        ! an array 'a', and 'adim1'.
        retval = CheckError(nf90_def_dim(this%ncid, name//"dim%4", &
                                         size(value,4), dimid4))
        dimids =  (/ dimid1, dimid2, dimid3, dimid4 /)
        retval = CheckError(nf90_def_var(this%ncid, name, NF90_DOUBLE, &
                                         dimids, this%var_id(this%next_var_index)))

        call this%PSyDataBaseType%DeclareArray4dDouble(name, value)

    end subroutine DeclareArray4dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine writes a 4D array of real(kind=real64)
    !! to the NetCDF file.
    !! @param[in,out] this The instance of the ExtractNetcdfBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine WriteArray4dDouble(this, name, value)

        use netcdf, only : nf90_put_var

        implicit none

        class(ExtractNetcdfBaseType), intent(inout), target :: this
        character(*), intent(in)                            :: name
        real(kind=real64), dimension(:,:,:,:), intent(in)      :: value

        integer :: retval

        if (.not. is_enabled) return
        if (this%verbosity >= 2) then
            write(stderr,*) "Writing Array Double."
        endif

retval = CheckError(nf90_put_var(this%ncid, this%var_id(this%next_var_index), &
                                         value(:,:,:,:)))
        call this%PSyDataBaseType%ProvideArray4dDouble(name, value)

    end subroutine WriteArray4dDouble


end module extract_netcdf_base_mod
