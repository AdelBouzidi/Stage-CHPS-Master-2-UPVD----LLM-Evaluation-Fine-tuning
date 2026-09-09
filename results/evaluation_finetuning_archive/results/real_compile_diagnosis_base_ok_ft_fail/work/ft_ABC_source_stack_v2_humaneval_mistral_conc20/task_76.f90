program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Hardcoded example input
  x = 8
  n = 2

  ! Call the function
  result = is_simple_power(x, n)

  ! Output the result
  print *, result

contains

  logical function is_simple_power(x, n)
    implicit none
    integer, intent(in) :: x, n
    integer :: i, count

    if (n == 0) then
       is_simple_power = .false.
       return
    end if

    if (x == 0) then
       is_simple_power = .false.
       return
    end if

    if (x == 1) then
       is_simple_power = .true.
       return
    end if

    if (n == 1) then
       is_simple_power = .false.
       return
    end if

    if (n == -1) then
       is_simple_power = .false.
       return
    end if

    if (x < 0) then
       is_simple_power = .false.
       return
    end if

    count = 0
    do while (x /= 1)
       if (mod(x, n) /= 0) then
          is_simple_power = .false.
          return
       end if
       x = x / n
       count = count + 1
    end do

    is_simple_power = .true.
  end function is_simple_power

end program is_simple_power_demo