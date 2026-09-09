program largest_prime_factor_demo
  implicit none
  integer :: n, result

  ! Read input number from stdin
  read(*,*) n

  ! Calculate largest prime factor
  result = largest_prime_factor(n)

  ! Output result
  print *, result

contains

  integer function largest_prime_factor(n)
    integer, intent(in) :: n
    integer :: i, temp
    temp = n
    largest_prime_factor = 2
    do while (temp > 1)
      if (mod(temp, i) == 0) then
        largest_prime_factor = i
        temp = temp / i
      else
        i = i + 1
      end if
    end do
  end function largest_prime_factor

end program largest_prime_factor_demo