program largest_divisor
  implicit none
  integer :: n, result

  ! Read input
  read *, n

  ! Find largest divisor smaller than n
  result = 1
  do while (n / 2 >= result)
    if (mod(n, n / 2) == 0) then
      result = n / 2
    end if
    n = n / 2
  end do

  ! Output result
  write (*, '(i0)') result

end program largest_divisor