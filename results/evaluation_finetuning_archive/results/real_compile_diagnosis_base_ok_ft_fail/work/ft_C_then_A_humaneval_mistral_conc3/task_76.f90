program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Read input from stdin
  read *, x
  read *, n

  result = is_simple_power(x, n)

  print *, 'is_simple_power(', x, ',', n, ') =', result

contains

  logical function is_simple_power(x, n)
    implicit none
    integer, intent(in) :: x, n
    integer :: i

    if (x == 1) then
       is_simple_power = .true.
       return
    end if

    if (n == 1) then
       is_simple_power = .false.
       return
    end if

    if (x < 1) then
       is_simple_power = .false.
       return
    end if

    do i = 1, x
       if (n**i == x) then
          is_simple_power = .true.
          return
       end if
    end do

    is_simple_power = .false.
  end function is_simple_power

end program is_simple_power_demo