program largest_prime_factor_demo
  implicit none
  integer :: n, result

  ! Hardcoded input value (example: 13195)
  n = 13195

  ! Call the function to get the largest prime factor
  result = largest_prime_factor(n)

  ! Output the result
  print *, result

contains

  function largest_prime_factor(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res, i, temp

    temp = n
    res = 2
    do while (temp > 1)
      if (mod(temp, res) == 0) then
        temp = temp / res
      else
        res = res + 1
      end if
    end do
  end function largest_prime_factor

end program largest_prime_factor_demo