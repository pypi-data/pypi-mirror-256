! ================================================== !
! THIS FILE IS CREATED FROM THE JINJA TEMPLATE FILE. !
! DO NOT MODIFY DIRECTLY!                            !
! ================================================== !




! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2020-2021, Science and Technology Facilities Council.
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
    subroutine profile_PSyDataInit()

      implicit none

      return

    end subroutine profile_PSyDataInit

    ! -------------------------------------------------------------------------
    !> @brief An optional initialisation subroutine.
    subroutine profile_PSyDataShutdown()

      implicit none

      return

    end subroutine profile_PSyDataShutdown

    ! -------------------------------------------------------------------------
    !> @brief Enables PSyData handling (if it is not already enabled).
    subroutine profile_PSyDataStart()

      implicit none

      is_enabled = .true.

    end subroutine profile_PSyDataStart

    ! -------------------------------------------------------------------------
    !> @brief Disables PSyData handling.
    subroutine profile_PSyDataStop()

      implicit none

      is_enabled = .false.

    end subroutine profile_PSyDataStop

    ! =========================================================================
    ! Jinja created code:
    ! =========================================================================

end module psy_data_base_mod
