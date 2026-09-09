program is_simple_power
  implicit none
  integer :: x, n
  logical :: result

  ! Read input
  read(*,*) x
  read(*,*) n

  ! Check if x is a simple power of n
  result = is_simple_power(x, n)

  ! Output result
  print *, result
contains

  function is_simple_power(x, n) result(result)
    implicit none
    integer, intent(in) :: x, n
    logical :: result
    integer :: k

    ! Handle edge cases
    if (n <= 0) then
      result = .false.
      return
    end if

    if (x <= 0) then
      result = .false.
      return
    end if

    if (x == 1) then
      result = .true.
      return
    end if

    if (n == 1) then
      result = .false.
      return
    end if

    ! Check if x is a power of n
    result = .false.
    do k = 1, 32
      if (n**k == x) then
        result = .true.
        exit
      end if
      if (n**k > x) then
        exit
      end if
    end do
  end function is_simple_power

end program is_simple_power