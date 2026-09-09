program is_simple_power_demo
  implicit none
  integer :: x
  logical :: result

  ! Read input from stdin
  read(*, *) x

  ! Call the function
  result = is_simple_power(x, 2)

  ! Output the result
  print *, result

contains

  logical function is_simple_power(x, n)
    implicit none
    integer, intent(in) :: x, n
    integer :: i, temp

    if (x <= 0) then
      is_simple_power = .false.
      return
    end if

    temp = x
    do i = 1, 30
      if (temp == 1) then
        is_simple_power = .true.
        return
      end if
      if (mod(temp, n) /= 0) then
        is_simple_power = .false.
        return
      end if
      temp = temp / n
    end do

    is_simple_power = .false.
  end function is_simple_power

end program is_simple_power_demo