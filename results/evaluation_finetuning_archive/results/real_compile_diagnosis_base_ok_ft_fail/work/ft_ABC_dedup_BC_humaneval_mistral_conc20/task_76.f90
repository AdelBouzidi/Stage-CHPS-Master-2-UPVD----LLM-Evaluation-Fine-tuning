program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Hardcoded input values
  x = 8
  n = 2

  result = is_simple_power(x, n)

  print *, 'is_simple_power(', x, ',', n, ') =', result
contains

  logical function is_simple_power(x, n)
    implicit none
    integer, intent(in) :: x, n
    integer :: i

    if (x <= 0) then
      is_simple_power = .false.
      return
    end if

    if (n <= 0) then
      is_simple_power = .false.
      return
    end if

    if (n == 1) then
      is_simple_power = (x == 1)
      return
    end if

    do i = 0, 30
      if (n**i == x) then
        is_simple_power = .true.
        return
      end if
      if (n**i > x) then
        is_simple_power = .false.
        return
      end if
    end do

    is_simple_power = .false.
  end function is_simple_power

end program is_simple_power_demo