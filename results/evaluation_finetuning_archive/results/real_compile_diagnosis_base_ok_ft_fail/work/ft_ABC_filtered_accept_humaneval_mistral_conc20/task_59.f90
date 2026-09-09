program largest_prime_factor_demo
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Calculate largest prime factor
  result = largest_prime_factor(n)

  ! Output result
  print *, result

contains

  function largest_prime_factor(n) result(res)
    integer, intent(in) :: n
    integer :: res
    integer :: i
    res = 2
    do while (n /= 1)
      if (mod(n, i) == 0) then
        res = i
        n = n / i
      else
        i = i + 1
      end if
    end do
  end function largest_prime_factor

end program largest_prime_factor_demo