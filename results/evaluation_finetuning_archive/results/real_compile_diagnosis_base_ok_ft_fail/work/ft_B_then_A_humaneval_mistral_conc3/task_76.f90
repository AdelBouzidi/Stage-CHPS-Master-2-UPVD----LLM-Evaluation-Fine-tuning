program main
  implicit none
  integer :: x
  read *, x
  print *, is_simple_power(x, 2)
contains
  logical function is_simple_power(x, n)
    integer, intent(in) :: x, n
    if (n == 0) then
      if (x == 1) then
        is_simple_power = .true.
      else
        is_simple_power = .false.
      end if
    else
      if (x == 1) then
        is_simple_power = .true.
      else if (x == 0) then
        is_simple_power = .false.
      else
        do while (x /= 1)
          if (mod(x, n) /= 0) then
            is_simple_power = .false.
            exit
          end if
          x = x / n
        end do
        is_simple_power = (x == 1)
      end if
    end if
  end function is_simple_power
end program main