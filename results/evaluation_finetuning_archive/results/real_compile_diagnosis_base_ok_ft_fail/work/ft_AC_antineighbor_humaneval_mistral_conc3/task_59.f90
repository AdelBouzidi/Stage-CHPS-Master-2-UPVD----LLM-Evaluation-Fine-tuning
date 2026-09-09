program largest_prime_factor_demo
  implicit none
  integer :: n, result

  ! Hardcoded input as per the example
  n = 13195

  result = largest_prime_factor(n)

  print *, 'Largest prime factor of', n, 'is', result

contains

  integer function largest_prime_factor(n)
    integer, intent(in) :: n
    integer :: i, factor

    factor = 2
    do while (factor * factor <= n)
      if (mod(n, factor) == 0) then
        n = n / factor
        do while (mod(n, factor) == 0)
          n = n / factor
        end do
        factor = factor + 1
      else
        factor = factor + 1
      end if
    end do
    largest_prime_factor = n
  end function largest_prime_factor

end program largest_prime_factor_demo