program largest_prime_factor_demo
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Calculate largest prime factor
  result = largest_prime_factor(n)

  ! Print output
  print *, result

contains

  integer function largest_prime_factor(n)
    integer, intent(in) :: n
    integer :: i
    largest_prime_factor = 2
    do i = 2, n
      if (mod(n, i) == 0) then
        largest_prime_factor = i
        n = n / i
        if (n == 1) exit
      end if
    end do
  end function largest_prime_factor

end program largest_prime_factor_demo