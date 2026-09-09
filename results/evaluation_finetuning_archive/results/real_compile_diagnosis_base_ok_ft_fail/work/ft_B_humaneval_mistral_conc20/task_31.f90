program is_prime
  implicit none
  integer :: n
  logical :: result
  integer :: i

  read *, n

  if (n <= 1) then
    result = .false.
  else if (n == 2) then
    result = .true.
  else if (mod(n, 2) == 0) then
    result = .false.
  else
    result = .true.
    i = 3
    do while (result .and. i * i <= n)
      if (mod(n, i) == 0) then
        result = .false.
      end if
      i = i + 2
    end do
  end if

  print *, result
end program is_prime