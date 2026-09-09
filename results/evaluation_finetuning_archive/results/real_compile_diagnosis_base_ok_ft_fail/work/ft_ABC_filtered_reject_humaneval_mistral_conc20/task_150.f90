program main
  implicit none
  integer :: n, x, y, result
  n = 7
  x = 34
  y = 12
  result = x_or_y(n, x, y)
  print *, result
contains
  integer function x_or_y(n, x, y)
    integer, intent(in) :: n, x, y
    if (is_prime(n)) then
      x_or_y = x
    else
      x_or_y = y
    end if
  end function x_or_y
  
  logical function is_prime(n)
    integer, intent(in) :: n
    if (n <= 1) then
      is_prime = .false.
    else if (n == 2) then
      is_prime = .true.
    else if (mod(n, 2) == 0) then
      is_prime = .false.
    else
      is_prime = .true.
      do while (is_prime .and. n > 2)
        if (mod(n, 2) == 0) then
          is_prime = .false.
        end if
        n = n / 2
      end do
    end if
  end function is_prime
end program main