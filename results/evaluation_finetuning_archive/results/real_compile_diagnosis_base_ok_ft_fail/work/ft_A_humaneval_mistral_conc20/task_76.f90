program main
  implicit none
  integer :: x, n
  logical :: result

  ! Read input
  read *, x
  read *, n

  ! Call the function
  result = is_simple_power(x, n)

  ! Output result
  print *, result

contains

  logical function is_simple_power(x, n)
    implicit none
    integer, intent(in) :: x, n
    integer :: k
    integer :: temp

    if (n == 0) then
      if (x == 1) then
        is_simple_power = .true.
      else
        is_simple_power = .false.
      end if
      return
    end if

    if (x == 1) then
      is_simple_power = .true.
      return
    end if

    if (x < 1) then
      is_simple_power = .false.
      return
    end if

    if (n < 1) then
      is_simple_power = .false.
      return
    end if

    temp = x
    k = 0
    do while (temp /= 1)
      if (mod(temp, n) /= 0) then
        is_simple_power = .false.
        return
      end if
      temp = temp / n
      k = k + 1
    end do

    is_simple_power = .true.

  end function is_simple_power

end program main