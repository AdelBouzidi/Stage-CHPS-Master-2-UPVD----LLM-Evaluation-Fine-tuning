program main
  implicit none
  integer :: n
  integer :: result

  ! Read input
  read(*,*) n

  ! Call the function
  result = largest_prime_factor(n)

  ! Print output
  print *, result

contains

  function largest_prime_factor(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i

    res = 2
    do while (n > 1)
      if (mod(n, i) == 0) then
        res = i
        n = n / i
      else
        i = i + 1
      end if
    end do
  end function largest_prime_factor

end program main