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
! Author J. Henrichs, Bureau of Meteorology
! Modified I. Kavcic, Met Office

!> This module implements a verification that read-only fields are
!! not overwritten (due to memory overwrites etc)
!!

module read_only_base_mod

    use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                              real32, real64, &
                                              stderr => Error_Unit
    use psy_data_base_mod, only : PSyDataBaseType, &
        read_only_verify_PSyDataShutdown, &
        read_only_verify_PSyDataInit, is_enabled, &
        read_only_verify_PSyDataStart, read_only_verify_PSyDataStop

    implicit none

    !> This is the data type that stores a checksum for each read-only
    !! variable. A static instance of this type is created for each
    !! instrumented region with PSyclone.

    type, extends(PSyDataBaseType), public :: ReadOnlyBaseType

        !> This field stores a 64-bit integer checksum for each
        !! variable.
        integer(kind=int64), dimension(:), allocatable :: checksums

        !> This boolean flag switches from 'computing and storing checksum'
        !! to 'verify checksum'.
        logical :: verify_checksums

    contains

        ! The various procedures used
        procedure :: PreStart
        procedure :: PreEndDeclaration
        procedure :: PostStart

        procedure :: ProvideScalarInt
        procedure :: ProvideArray2dInt
        procedure :: ProvideScalarReal
        procedure :: ProvideArray2dReal
        procedure :: ProvideScalarDouble
        procedure :: ProvideArray2dDouble


        !> The generic interface for providing the value of variables,
        !! which in case of the read-only verification either computes
        !! the checksum (before a kernel), or compares a checksum (after
        !! a kernel call). The generic interface is only defined if
        !! explicitly requested. This allows a derived class to implement
        !! its own functions and provide them as part of the generic
        !! interface.
        generic, public :: ProvideVariable => &
            ProvideScalarInt, &
            ProvideArray2dInt, &
            ProvideScalarReal, &
            ProvideArray2dReal, &
            ProvideScalarDouble, &
            ProvideArray2dDouble

    end type ReadOnlyBaseType


    ! Generic interface for all ComputeChecksum functions
    interface ComputeChecksum
      module procedure &
        ComputeChecksum2dInt, &
        ComputeChecksum2dReal, &
        ComputeChecksum2dDouble
    end interface ComputeChecksum

    public ComputeChecksum

contains

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is the first function called when an instrumented region
    !! is entered. It initialises this object, and stores module and regin
    !! names.
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    !! @param[in] module_name The name of the module of the instrumented
    !!            region.
    !! @param[in] kernel_name The name of the instrumented region.
    !! @param[in] num_pre_vars The number of variables that are declared and
    !!            checksum'ed before the instrumented region.
    !! @param[in] num_post_vars The number of variables that are also declared
    !!            before an instrumented region of code, but are checksum'ed
    !!            after this region.
    subroutine PreStart(this, module_name, region_name, num_pre_vars, &
                        num_post_vars)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        character(*), intent(in) :: module_name, region_name
        integer, intent(in)      :: num_pre_vars, num_post_vars

        character(1) :: verbose
        integer :: status

        call this%PSyDataBaseType%PreStart(module_name, region_name, &
                                           num_pre_vars, num_post_vars)
        this%verify_checksums = .false.

        if (.not. is_enabled) return

        if (num_pre_vars /= num_post_vars) then
            write(stderr, *) "PSyData: The same number of variables must be provided before"
            write(stderr, *) "and after the instrumented region. But the values are:"
            write(stderr, *) "Before: ", num_pre_vars, " after: ", num_post_vars
            call this%Abort("PreStart: Inconsistent parameters")
        endif

    end subroutine PreStart

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called once all variables are declared. It makes
    !! sure that the next variable index is starting at 1 again.
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    subroutine PreEndDeclaration(this)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        integer :: err

        if (.not. is_enabled) return

        ! During the declaration the number of checksums to be
        ! stored was counted in next_var_index, so allocate the array
        ! now (if it has not been allocated already in a previous call):
        if (.not. allocated(this%checksums)) then
            allocate(this%checksums(this%next_var_index-1), stat=err)
            if(err/=0) then
                write(stderr, *) "PSyData: Could not allocate ", &
                                 this%next_var_index-1,          &
                                 " integers, aborting."
                call this%Abort("Out of memory")
            endif
        endif

        call this%PSyDataBaseType%PreEndDeclaration()

    end subroutine PreEndDeclaration

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called after the instrumented region has been
    !! executed. After this call the value of variables after the instrumented
    !! region will be provided. This subroutine sets the 'verify_checksum'
    !! flag to true, causing all further checksum calls to verify that the
    !! checksum has not changed. It also resets the next variable index to 1
    !! again.
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    subroutine PostStart(this)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this

        call this%PSyDataBaseType%PostStart()
        ! The pointer mst be reset to 1 to make sure we compare
        ! with the previously computed checksums
        this%next_var_index = 1
        this%verify_checksums = .true.

    end subroutine PostStart


    ! =========================================================================
    ! Jinja created code.
    ! =========================================================================



    ! =========================================================================
    ! Implementation for all integer(kind=int32) types
    ! =========================================================================
    ! -------------------------------------------------------------------------
    !> @brief This subroutine either computes a checksum or compares a checksum
    !! (depending on this%verify_checksums) for a single Int.
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarInt(this, name, value)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), intent(in)     :: value

        integer(kind=int32)            :: orig_value
        integer(kind=int64) :: checksum, int_64

        integer(kind=int32) :: int_32

        if (.not. is_enabled) return

        ! `transfer` leaves undefined bits in a 64-bit value
        ! so assign to 32-bit, then assign to 64-bit to have all bits defined
        int_32 = transfer(value, int_32)
        checksum = int_32

        if (this%verify_checksums) then
            if (checksum /= this%checksums(this%next_var_index)) then
                write(stderr,*) "------------- PSyData -------------------------"
                write(stderr,*) "integer(kind=int32) variable ", name, " has been modified in ", &
                    trim(this%module_name)," : ", trim(this%region_name)
                ! We can recreate the original value which is stored as
                ! 64-bit integer as the checksum:
                int_32 = this%checksums(this%next_var_index)
                orig_value = transfer(int_32, orig_value)
                write(stderr,*) "Original value: ", orig_value
                write(stderr,*) "New value:      ", value
                write(stderr,*) "------------- PSyData -------------------------"
            else if(this%verbosity>1) then
                write(stderr,*) "PSyData: checked variable ", trim(name)
            endif
        else
            this%checksums(this%next_var_index) = checksum
        endif

        call this%PSyDataBaseType%ProvideScalarInt(name, value)

    end subroutine ProvideScalarInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine either computes a checksum or compares a checksum
    !! (depending on this%verify_checksums) for a 2D array of integer
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dInt(this, name, value)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:), intent(in) :: value
        integer(kind=int64) :: checksum
        integer :: i, j

        if (.not. is_enabled) return

        checksum = ComputeChecksum(value)
        if (this%verify_checksums) then
            if (checksum /= this%checksums(this%next_var_index)) then
                write(stderr,*) "------------- PSyData -------------------------"
                write(stderr,*) "2d Int array ", name, " has been modified in ", &
                    trim(this%module_name)," : ", trim(this%region_name)
                write(stderr,*) "Original checksum: ", this%checksums(this%next_var_index)
                write(stderr,*) "New checksum:      ", checksum
                write(stderr,*) "------------- PSyData -------------------------"
            else if(this%verbosity>1) then
                write(stderr,*) "PSyData: checked variable ", trim(name)
            endif
        else
            this%checksums(this%next_var_index) = checksum
        endif

        call this%PSyDataBaseType%ProvideArray2dInt(name, value)

    end subroutine ProvideArray2dInt


    ! -------------------------------------------------------------------------
    !> @brief This function computes a 64-bit integer checksum for a 2D
    !! integer(kind=int32) Fortran array.
    function ComputeChecksum2dInt(field) result(checksum)

        implicit none

        integer(kind=int32), dimension(:,:) :: field

        integer :: i1,i2
        integer(kind=int32) :: int_32
        integer(kind=int64) :: checksum, int_64

        checksum = 0
        do i2=1, size(field, 2)
           do i1=1, size(field, 1)
              ! transfer leaves undefined bits in a 64-bit target
              ! so we transfer to 32-bits and then assign to 64-bit
              int_32 = transfer(field(i1,i2), int_32)
              int_64 = int_32
              checksum = checksum + int_64
           enddo
        enddo

    end function ComputeChecksum2dInt


    ! =========================================================================
    ! Implementation for all real(kind=real32) types
    ! =========================================================================
    ! -------------------------------------------------------------------------
    !> @brief This subroutine either computes a checksum or compares a checksum
    !! (depending on this%verify_checksums) for a single Real.
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarReal(this, name, value)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), intent(in)     :: value

        real(kind=real32)            :: orig_value
        integer(kind=int64) :: checksum, int_64

        integer(kind=int32) :: int_32

        if (.not. is_enabled) return

        ! `transfer` leaves undefined bits in a 64-bit value
        ! so assign to 32-bit, then assign to 64-bit to have all bits defined
        int_32 = transfer(value, int_32)
        checksum = int_32

        if (this%verify_checksums) then
            if (checksum /= this%checksums(this%next_var_index)) then
                write(stderr,*) "------------- PSyData -------------------------"
                write(stderr,*) "real(kind=real32) variable ", name, " has been modified in ", &
                    trim(this%module_name)," : ", trim(this%region_name)
                ! We can recreate the original value which is stored as
                ! 64-bit integer as the checksum:
                int_32 = this%checksums(this%next_var_index)
                orig_value = transfer(int_32, orig_value)
                write(stderr,*) "Original value: ", orig_value
                write(stderr,*) "New value:      ", value
                write(stderr,*) "------------- PSyData -------------------------"
            else if(this%verbosity>1) then
                write(stderr,*) "PSyData: checked variable ", trim(name)
            endif
        else
            this%checksums(this%next_var_index) = checksum
        endif

        call this%PSyDataBaseType%ProvideScalarReal(name, value)

    end subroutine ProvideScalarReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine either computes a checksum or compares a checksum
    !! (depending on this%verify_checksums) for a 2D array of integer
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dReal(this, name, value)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:), intent(in) :: value
        integer(kind=int64) :: checksum
        integer :: i, j

        if (.not. is_enabled) return

        checksum = ComputeChecksum(value)
        if (this%verify_checksums) then
            if (checksum /= this%checksums(this%next_var_index)) then
                write(stderr,*) "------------- PSyData -------------------------"
                write(stderr,*) "2d Real array ", name, " has been modified in ", &
                    trim(this%module_name)," : ", trim(this%region_name)
                write(stderr,*) "Original checksum: ", this%checksums(this%next_var_index)
                write(stderr,*) "New checksum:      ", checksum
                write(stderr,*) "------------- PSyData -------------------------"
            else if(this%verbosity>1) then
                write(stderr,*) "PSyData: checked variable ", trim(name)
            endif
        else
            this%checksums(this%next_var_index) = checksum
        endif

        call this%PSyDataBaseType%ProvideArray2dReal(name, value)

    end subroutine ProvideArray2dReal


    ! -------------------------------------------------------------------------
    !> @brief This function computes a 64-bit integer checksum for a 2D
    !! real(kind=real32) Fortran array.
    function ComputeChecksum2dReal(field) result(checksum)

        implicit none

        real(kind=real32), dimension(:,:) :: field

        integer :: i1,i2
        integer(kind=int32) :: int_32
        integer(kind=int64) :: checksum, int_64

        checksum = 0
        do i2=1, size(field, 2)
           do i1=1, size(field, 1)
              ! transfer leaves undefined bits in a 64-bit target
              ! so we transfer to 32-bits and then assign to 64-bit
              int_32 = transfer(field(i1,i2), int_32)
              int_64 = int_32
              checksum = checksum + int_64
           enddo
        enddo

    end function ComputeChecksum2dReal


    ! =========================================================================
    ! Implementation for all real(kind=real64) types
    ! =========================================================================
    ! -------------------------------------------------------------------------
    !> @brief This subroutine either computes a checksum or compares a checksum
    !! (depending on this%verify_checksums) for a single Double.
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarDouble(this, name, value)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), intent(in)     :: value

        real(kind=real64)            :: orig_value
        integer(kind=int64) :: checksum, int_64


        if (.not. is_enabled) return

        checksum = transfer(value, int_64)

        if (this%verify_checksums) then
            if (checksum /= this%checksums(this%next_var_index)) then
                write(stderr,*) "------------- PSyData -------------------------"
                write(stderr,*) "real(kind=real64) variable ", name, " has been modified in ", &
                    trim(this%module_name)," : ", trim(this%region_name)
                ! We can recreate the original value which is stored as
                ! 64-bit integer as the checksum:
                orig_value = transfer(this%checksums(this%next_var_index), orig_value)
                write(stderr,*) "Original value: ", orig_value
                write(stderr,*) "New value:      ", value
                write(stderr,*) "------------- PSyData -------------------------"
            else if(this%verbosity>1) then
                write(stderr,*) "PSyData: checked variable ", trim(name)
            endif
        else
            this%checksums(this%next_var_index) = checksum
        endif

        call this%PSyDataBaseType%ProvideScalarDouble(name, value)

    end subroutine ProvideScalarDouble

    ! -------------------------------------------------------------------------
    !> @brief This subroutine either computes a checksum or compares a checksum
    !! (depending on this%verify_checksums) for a 2D array of integer
    !! @param[in,out] this The instance of the ReadOnlyBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dDouble(this, name, value)

        implicit none

        class(ReadOnlyBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:), intent(in) :: value
        integer(kind=int64) :: checksum
        integer :: i, j

        if (.not. is_enabled) return

        checksum = ComputeChecksum(value)
        if (this%verify_checksums) then
            if (checksum /= this%checksums(this%next_var_index)) then
                write(stderr,*) "------------- PSyData -------------------------"
                write(stderr,*) "2d Double array ", name, " has been modified in ", &
                    trim(this%module_name)," : ", trim(this%region_name)
                write(stderr,*) "Original checksum: ", this%checksums(this%next_var_index)
                write(stderr,*) "New checksum:      ", checksum
                write(stderr,*) "------------- PSyData -------------------------"
            else if(this%verbosity>1) then
                write(stderr,*) "PSyData: checked variable ", trim(name)
            endif
        else
            this%checksums(this%next_var_index) = checksum
        endif

        call this%PSyDataBaseType%ProvideArray2dDouble(name, value)

    end subroutine ProvideArray2dDouble


    ! -------------------------------------------------------------------------
    !> @brief This function computes a 64-bit integer checksum for a 2D
    !! real(kind=real64) Fortran array.
    function ComputeChecksum2dDouble(field) result(checksum)

        implicit none

        real(kind=real64), dimension(:,:) :: field

        integer :: i1,i2
        integer(kind=int64) :: checksum, int_64

        checksum = 0
        do i2=1, size(field, 2)
           do i1=1, size(field, 1)
              int_64 = transfer(field(i1,i2), checksum)
              checksum = checksum + int_64
           enddo
        enddo

    end function ComputeChecksum2dDouble

    ! -------------------------------------------------------------------------

end module read_only_base_mod
