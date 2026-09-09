program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Read input from stdin
  read(*,*) x, n

  ! Call the function
  result = is_simple_power(x, n)

  ! Output the result
  print *, result

contains

  logical function is_simple_power(x, n)
    integer, intent(in) :: x, n
    integer :: i

    if (n <= 0) then
      is_simple_power = .false.
      return
    end if

    if (x <= 0) then
      is_simple_power = .false.
      return
    end if

    if (n == 1) then
      is_simple_power = (x == 1)
      return
    end if

    do i = 1, 32
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