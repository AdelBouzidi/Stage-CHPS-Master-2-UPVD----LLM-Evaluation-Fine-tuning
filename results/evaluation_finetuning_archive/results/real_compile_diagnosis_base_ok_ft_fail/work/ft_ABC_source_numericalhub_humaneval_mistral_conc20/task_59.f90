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

  function largest_prime_factor(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i

    res = 2
    i = 2
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