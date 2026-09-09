program largest_prime_factor_demo
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Call the function
  result = largest_prime_factor(n)

  ! Write output to stdout
  print *, result

contains

  integer function largest_prime_factor(n)
    integer, intent(in) :: n
    integer :: i, factor

    factor = 2
    do while (factor * factor <= n)
      if (mod(n, factor) == 0) then
        n = n / factor
        factor = factor + 1
      else
        factor = factor + 1
      end if
    end do
    largest_prime_factor = n
  end function largest_prime_factor

end program largest_prime_factor_demo