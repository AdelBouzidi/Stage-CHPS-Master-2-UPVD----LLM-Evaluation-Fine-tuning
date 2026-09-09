program largest_prime_factor_demo
  implicit none
  integer :: n
  integer :: result

  ! Read input from stdin
  read(*,*) n

  ! Calculate largest prime factor
  result = largest_prime_factor(n)

  ! Output result
  print *, result

contains

  function largest_prime_factor(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i
    res = 1
    do i = 2, n
      if (mod(n, i) == 0) then
        res = i
      end if
    end do
  end function largest_prime_factor

end program largest_prime_factor_demo