program largest_prime_factor
  implicit none
  integer :: n, result

  ! Hardcoded input as per requirements
  n = 13195

  result = largest_prime_factor(n)

  print *, 'Largest prime factor of', n, 'is', result
contains

  integer function largest_prime_factor(n)
    integer, intent(in) :: n
    integer :: i
    largest_prime_factor = 1
    do i = 2, n
      if (mod(n, i) == 0) then
        largest_prime_factor = i
        n = n / i
        if (n == 1) exit
      end if
    end do
  end function largest_prime_factor

end program largest_prime_factor