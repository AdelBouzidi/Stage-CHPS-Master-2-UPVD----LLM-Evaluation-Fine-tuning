program largest_prime_factor
  implicit none
  integer :: n, result

  ! Read input number
  read *, n

  ! Calculate largest prime factor
  result = largest_prime_factor(n)

  ! Output result
  print *, result

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