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

module psy_data_base_mod

    use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                              real32, real64, &
                                              stderr => Error_Unit
    implicit none

    !> Maximum string length for module- and region-names
    integer, parameter :: MAX_STRING_LENGTH = 512

    !> If this section is enabled or not. Controlled by the two
    !! static functions PSyDataStart and PSyDataStop. Note that
    !! none of the functions here use this value at all, it is up
    !! to the derived classes to implement the start/stop functionality.
    logical :: is_enabled = .true.

    !> This is a useful base class for PSyData wrapper libraries.
    !! It is not required to use this as a base, but it provides
    !! useful functionality.

    type, public:: PSyDataBaseType

        !> The index of the variables as they are being declared
        !! and as they are being provided. It is useful to provided
        !! a variable-dependent index.
        integer :: next_var_index

        !> Verbosity level for output at runtime. This is taken from the
        !! PSYDATA_VERBOSE environment variable.
        !! 0: Only errors will be written (PSYDATA_VERBOSE undefined)
        !! 1: Additionally write the name of the confirmed kernel_name
        !! 2: Also write the name of each tested variable
        integer :: verbosity

        !> Store the name of the module and region
        character(MAX_STRING_LENGTH) :: module_name, region_name

        contains

            procedure :: PreStart
            procedure :: PreEndDeclaration
            procedure :: PreEnd
            procedure :: PostStart
            procedure :: PostEnd
            procedure :: Abort

            procedure :: DeclareScalarChar
            procedure :: ProvideScalarChar
            procedure :: DeclareArray1dChar
            procedure :: ProvideArray1dChar
            procedure :: DeclareArray2dChar
            procedure :: ProvideArray2dChar
            procedure :: DeclareArray3dChar
            procedure :: ProvideArray3dChar
            procedure :: DeclareArray4dChar
            procedure :: ProvideArray4dChar
            procedure :: DeclareScalarInt
            procedure :: ProvideScalarInt
            procedure :: DeclareArray1dInt
            procedure :: ProvideArray1dInt
            procedure :: DeclareArray2dInt
            procedure :: ProvideArray2dInt
            procedure :: DeclareArray3dInt
            procedure :: ProvideArray3dInt
            procedure :: DeclareArray4dInt
            procedure :: ProvideArray4dInt
            procedure :: DeclareScalarLong
            procedure :: ProvideScalarLong
            procedure :: DeclareArray1dLong
            procedure :: ProvideArray1dLong
            procedure :: DeclareArray2dLong
            procedure :: ProvideArray2dLong
            procedure :: DeclareArray3dLong
            procedure :: ProvideArray3dLong
            procedure :: DeclareArray4dLong
            procedure :: ProvideArray4dLong
            procedure :: DeclareScalarLogical
            procedure :: ProvideScalarLogical
            procedure :: DeclareArray1dLogical
            procedure :: ProvideArray1dLogical
            procedure :: DeclareArray2dLogical
            procedure :: ProvideArray2dLogical
            procedure :: DeclareArray3dLogical
            procedure :: ProvideArray3dLogical
            procedure :: DeclareArray4dLogical
            procedure :: ProvideArray4dLogical
            procedure :: DeclareScalarReal
            procedure :: ProvideScalarReal
            procedure :: DeclareArray1dReal
            procedure :: ProvideArray1dReal
            procedure :: DeclareArray2dReal
            procedure :: ProvideArray2dReal
            procedure :: DeclareArray3dReal
            procedure :: ProvideArray3dReal
            procedure :: DeclareArray4dReal
            procedure :: ProvideArray4dReal
            procedure :: DeclareScalarDouble
            procedure :: ProvideScalarDouble
            procedure :: DeclareArray1dDouble
            procedure :: ProvideArray1dDouble
            procedure :: DeclareArray2dDouble
            procedure :: ProvideArray2dDouble
            procedure :: DeclareArray3dDouble
            procedure :: ProvideArray3dDouble
            procedure :: DeclareArray4dDouble
            procedure :: ProvideArray4dDouble



    end type PSyDataBaseType

contains

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is the first function called when an instrumented region
    !! is entered. It initialises this object, and stores module and regin
    !! names.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] module_name The name of the module of the instrumented
    !!            region.
    !! @param[in] region_name The name of the instrumented region.
    !! @param[in] num_pre_vars The number of variables that are declared and
    !!            written before the instrumented region (unused atm).
    !! @param[in] num_post_vars The number of variables that are also declared
    !!            before an instrumented region of code, but are written after
    !!            this region (unused atm).
    subroutine PreStart(this, module_name, region_name, num_pre_vars, &
                        num_post_vars)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: module_name, region_name
        integer, intent(in)      :: num_pre_vars, num_post_vars

        character(1) :: verbose
        integer      :: status

        call get_environment_variable("PSYDATA_VERBOSE", verbose, status=status)
        this%verbosity = 0
        if (status == 0) then
            if (verbose == "0") then
                this%verbosity = 0
            else if (verbose == "1") then
                this%verbosity = 1
            else if (verbose == "2") then
                this%verbosity = 2
            else
                write(stderr,*) "PSyData: invalid setting of PSYDATA_VERBOSE."
                write(stderr,*) "It must be '0', 1' or '2', but it is '", verbose,"'."
                this%verbosity = 0
            endif
        endif

        this%next_var_index = 1
        this%module_name = module_name
        this%region_name = region_name

        if (.not. is_enabled) return

        if (this%verbosity > 0) &
            write(stderr,*) "PSyData: PreStart ", module_name, " ", region_name

    end subroutine PreStart

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called once all variables are declared. It makes
    !! sure that the next variable index is starting at 1 again.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    subroutine PreEndDeclaration(this)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this

        this%next_var_index = 1

    end subroutine PreEndDeclaration

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called after the value of all variables has been
    !! provided (and declared). After this call the instrumented region will
    !! be executed. Nothing is done here.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    subroutine PreEnd(this)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this

    end subroutine PreEnd

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called after the instrumented region has been
    !! executed. After this call the value of variables after the instrumented
    !! region will be provided. Nothing is done here.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    subroutine PostStart(this)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this

    end subroutine PostStart

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called after the instrumented region has been
    !! executed and all values of variables after the instrumented
    !! region have been provided. No special functionality required here.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    subroutine PostEnd(this)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this

        if (.not. is_enabled) return

        if (this%verbosity > 0) &
            write(stderr, *) "PSyData: PostEnd ", trim(this%module_name), &
                    " ", trim(this%region_name)

    end subroutine PostEnd

    ! -------------------------------------------------------------------------
    !> @brief Displays the message and aborts execution. This base implementation
    !! just uses `stop`.
    !! @param[in] message Error message to be displayed (string).
    subroutine Abort(this, message)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*) :: message

        write(stderr, *) "PSyData Error:", message
        stop "PSyData: Aborting"

    end subroutine Abort

    ! -------------------------------------------------------------------------
    !> @brief An optional initialisation subroutine.
    subroutine extract_PSyDataInit()

      implicit none

      return

    end subroutine extract_PSyDataInit

    ! -------------------------------------------------------------------------
    !> @brief An optional initialisation subroutine.
    subroutine extract_PSyDataShutdown()

      implicit none

      return

    end subroutine extract_PSyDataShutdown

    ! -------------------------------------------------------------------------
    !> @brief Enables PSyData handling (if it is not already enabled).
    subroutine extract_PSyDataStart()

      implicit none

      is_enabled = .true.

    end subroutine extract_PSyDataStart

    ! -------------------------------------------------------------------------
    !> @brief Disables PSyData handling.
    subroutine extract_PSyDataStop()

      implicit none

      is_enabled = .false.

    end subroutine extract_PSyDataStop

    ! =========================================================================
    ! Jinja created code:
    ! =========================================================================
    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar character(*) value. This
    !! implementation only increases the next index, and prints
    !! the name of the variable if verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), intent(in) :: value

        this%next_var_index = this%next_var_index+1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareScalarChar: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareScalarChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine provides a scalar character(*) value. This
    !! implementation only increases the next index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), intent(in) :: value

        this%next_var_index = this%next_var_index+1

    end subroutine ProvideScalarChar

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 1D array of
    !! character(*) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray1dChar: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray1dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 1D character(*) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray1dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray1dChar

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 2D array of
    !! character(*) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray2dChar: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray2dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 2D character(*) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray2dChar

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 3D array of
    !! character(*) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray3dChar: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray3dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 3D character(*) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray3dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray3dChar

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 4D array of
    !! character(*) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:,:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray4dChar: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray4dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 4D character(*) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray4dChar(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        character(*), dimension(:,:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray4dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar integer(kind=int32) value. This
    !! implementation only increases the next index, and prints
    !! the name of the variable if verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), intent(in) :: value

        this%next_var_index = this%next_var_index+1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareScalarInt: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareScalarInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine provides a scalar integer(kind=int32) value. This
    !! implementation only increases the next index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), intent(in) :: value

        this%next_var_index = this%next_var_index+1

    end subroutine ProvideScalarInt

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 1D array of
    !! integer(kind=int32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray1dInt: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray1dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 1D integer(kind=int32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray1dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray1dInt

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 2D array of
    !! integer(kind=int32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray2dInt: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray2dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 2D integer(kind=int32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray2dInt

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 3D array of
    !! integer(kind=int32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray3dInt: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray3dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 3D integer(kind=int32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray3dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray3dInt

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 4D array of
    !! integer(kind=int32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray4dInt: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray4dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 4D integer(kind=int32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray4dInt(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray4dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar integer(kind=int64) value. This
    !! implementation only increases the next index, and prints
    !! the name of the variable if verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), intent(in) :: value

        this%next_var_index = this%next_var_index+1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareScalarLong: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareScalarLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine provides a scalar integer(kind=int64) value. This
    !! implementation only increases the next index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), intent(in) :: value

        this%next_var_index = this%next_var_index+1

    end subroutine ProvideScalarLong

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 1D array of
    !! integer(kind=int64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray1dLong: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray1dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 1D integer(kind=int64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray1dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray1dLong

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 2D array of
    !! integer(kind=int64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray2dLong: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray2dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 2D integer(kind=int64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray2dLong

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 3D array of
    !! integer(kind=int64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray3dLong: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray3dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 3D integer(kind=int64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray3dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray3dLong

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 4D array of
    !! integer(kind=int64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:,:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray4dLong: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray4dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 4D integer(kind=int64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray4dLong(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int64), dimension(:,:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray4dLong

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar Logical(kind=4) value. This
    !! implementation only increases the next index, and prints
    !! the name of the variable if verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), intent(in) :: value

        this%next_var_index = this%next_var_index+1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareScalarLogical: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareScalarLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine provides a scalar Logical(kind=4) value. This
    !! implementation only increases the next index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), intent(in) :: value

        this%next_var_index = this%next_var_index+1

    end subroutine ProvideScalarLogical

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 1D array of
    !! Logical(kind=4) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray1dLogical: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray1dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 1D Logical(kind=4) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray1dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray1dLogical

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 2D array of
    !! Logical(kind=4) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray2dLogical: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray2dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 2D Logical(kind=4) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray2dLogical

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 3D array of
    !! Logical(kind=4) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray3dLogical: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray3dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 3D Logical(kind=4) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray3dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray3dLogical

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 4D array of
    !! Logical(kind=4) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:,:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray4dLogical: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray4dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 4D Logical(kind=4) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray4dLogical(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        Logical(kind=4), dimension(:,:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray4dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar real(kind=real32) value. This
    !! implementation only increases the next index, and prints
    !! the name of the variable if verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), intent(in) :: value

        this%next_var_index = this%next_var_index+1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareScalarReal: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareScalarReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine provides a scalar real(kind=real32) value. This
    !! implementation only increases the next index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), intent(in) :: value

        this%next_var_index = this%next_var_index+1

    end subroutine ProvideScalarReal

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 1D array of
    !! real(kind=real32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray1dReal: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray1dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 1D real(kind=real32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray1dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray1dReal

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 2D array of
    !! real(kind=real32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray2dReal: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray2dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 2D real(kind=real32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray2dReal

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 3D array of
    !! real(kind=real32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray3dReal: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray3dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 3D real(kind=real32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray3dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray3dReal

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 4D array of
    !! real(kind=real32) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray4dReal: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray4dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 4D real(kind=real32) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray4dReal(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray4dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine declares a scalar real(kind=real64) value. This
    !! implementation only increases the next index, and prints
    !! the name of the variable if verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareScalarDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), intent(in) :: value

        this%next_var_index = this%next_var_index+1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareScalarDouble: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareScalarDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine provides a scalar real(kind=real64) value. This
    !! implementation only increases the next index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), intent(in) :: value

        this%next_var_index = this%next_var_index+1

    end subroutine ProvideScalarDouble

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 1D array of
    !! real(kind=real64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray1dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray1dDouble: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray1dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 1D real(kind=real64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray1dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray1dDouble

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 2D array of
    !! real(kind=real64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray2dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray2dDouble: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray2dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 2D real(kind=real64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray2dDouble

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 3D array of
    !! real(kind=real64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray3dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray3dDouble: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray3dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 3D real(kind=real64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray3dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray3dDouble

    ! ---------------------------------------------------------------------
    !> @brief This subroutine handles a declaration of a 4D array of
    !! real(kind=real64) values. This base implementation only increases
    !! next_var_index and prints the name of the variable if
    !! verbose output is requested.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareArray4dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:,:,:), intent(in) :: value
        this%next_var_index = this%next_var_index + 1

        if (.not. is_enabled) return

        if (this%verbosity > 1) &
            write(stderr,*) "PSyData: DeclareArray4dDouble: ", &
                            trim(this%module_name), " ", &
                            trim(this%region_name), ": ", name

    end subroutine DeclareArray4dDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine handles a provide call for a 4D real(kind=real64) array.
    !! This base implementation only increases next_var_index.
    !! @param[in,out] this The instance of the PSyDataBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray4dDouble(this, name, value)

        implicit none

        class(PSyDataBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:,:,:), intent(in) :: value

        this%next_var_index = this%next_var_index + 1

    end subroutine ProvideArray4dDouble


end module psy_data_base_mod
