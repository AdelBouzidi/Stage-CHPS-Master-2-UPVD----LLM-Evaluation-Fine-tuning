program main
  implicit none
  integer :: x, n
  logical :: result

  ! Read input
  read(*,*) x
  read(*,*) n

  ! Call the function
  result = is_simple_power(x, n)

  ! Print output
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

    if (n == 2) then
      is_simple_power = (x == 2**i)
      return
    end if

    is_simple_power = .false.
  end function is_simple_power

end program main