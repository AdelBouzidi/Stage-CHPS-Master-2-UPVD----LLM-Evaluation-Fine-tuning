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

  function largest_prime_factor(n) result(res)
    integer, intent(in) :: n
    integer :: res
    integer :: i

    res = 2
    i = 2
    do while (i * i <= n)
      if (mod(n, i) == 0) then
        res = i
        n = n / i
      else
        i = i + 1
      end if
    end do
    if (n > 1) then
      res = n
    end if
  end function largest_prime_factor

end program largest_prime_factor