program largest_prime_factor
  implicit none
  integer :: n, result

  ! Hardcoded input as per the problem statement
  n = 13195

  result = largest_prime_factor(n)

  print *, 'Largest prime factor of', n, 'is', result
contains

  integer function largest_prime_factor(n)
    integer, intent(in) :: n
    integer :: i, temp
    temp = n
    largest_prime_factor = 2
    do while (temp > 1)
      if (mod(temp, largest_prime_factor) == 0) then
        temp = temp / largest_prime_factor
      else
        largest_prime_factor = largest_prime_factor + 1
      end if
    end do
  end function largest_prime_factor

end program largest_prime_factor