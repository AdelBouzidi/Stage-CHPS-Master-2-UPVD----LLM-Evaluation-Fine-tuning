program prime_check
  implicit none
  integer :: n
  logical :: result

  ! Read input
  read(*,*) n

  ! Call the function
  result = is_prime(n)

  ! Output result
  print *, result

contains

  function is_prime(n) result(res)
    implicit none
    integer, intent(in) :: n
    logical :: res
    integer :: i

    if (n < 2) then
      res = .false.
    else if (n == 2) then
      res = .true.
    else if (mod(n, 2) == 0) then
      res = .false.
    else
      res = .true.
      do i = 3, int(sqrt(real(n, kind=real(0, kind=n))))
        if (mod(n, i) == 0) then
          res = .false.
          exit
        end if
      end do
    end if
  end function is_prime

end program prime_check