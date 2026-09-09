program is_simple_power
  implicit none
  integer :: x, n, result
  
  read *, x, n
  
  if (n <= 0) then
    result = .false.
  else if (x <= 0) then
    result = .false.
  else if (x == 1) then
    result = .true.
  else if (mod(x, n) == 0) then
    result = .true.
    do while (x /= 1)
      x = x / n
    end do
  else
    result = .false.
  end if
  
  print *, result
end program is_simple_power