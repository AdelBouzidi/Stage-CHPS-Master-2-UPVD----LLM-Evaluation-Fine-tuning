program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Read input
  read(*,*) x, n

  ! Call the function
  result = is_simple_power(x, n)

  ! Output result
  print *, result

contains

  logical function is_simple_power(x, n)
    integer, intent(in) :: x, n
    integer :: temp

    if (x == 1) then
      is_simple_power = .true.
      return
    end if

    if (x == 0) then
      if (n == 0) then
        is_simple_power = .true.
      else
        is_simple_power = .false.
      end if
      return
    end if

    if (n == 0) then
      is_simple_power = .false.
      return
    end if

    if (n < 0) then
      is_simple_power = .false.
      return
    end if

    temp = x
    is_simple_power = .true.
    do while (temp /= 1)
      if (mod(temp, n) /= 0) then
        is_simple_power = .false.
        return
      end if
      temp = temp / n
    end do

  end function is_simple_power

end program is_simple_power_demo