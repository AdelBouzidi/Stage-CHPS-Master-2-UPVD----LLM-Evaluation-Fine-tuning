program largest_prime_factor
  implicit none
  integer :: n, result

  ! Hardcoded input as per example
  n = 13195

  result = largest_prime_factor(n)

  print *, 'Largest prime factor of', n, 'is', result
end program largest_prime_factor