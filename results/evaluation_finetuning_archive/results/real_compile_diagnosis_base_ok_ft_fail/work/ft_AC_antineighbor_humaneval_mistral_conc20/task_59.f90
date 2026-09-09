program largest_prime_factor
  implicit none
  integer :: n, i, largest_factor

  ! Read input number
  read *, n

  ! Find largest prime factor
  largest_factor = 2
  do i = 2, n
    if (mod(n, i) == 0) then
      largest_factor = i
      n = n / i
      if (n == 1) exit
    end if
  end do

  ! Output result
  print *, largest_factor

end program largest_prime_factor