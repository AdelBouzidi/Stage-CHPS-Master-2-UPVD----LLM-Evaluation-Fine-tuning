program main
  implicit none
  integer :: n, x, y
  integer :: i
  logical :: is_prime

  ! Read input
  read *, n
  read *, x
  read *, y

  ! Check if n is prime
  is_prime = .true.
  if (n <= 1) then
    is_prime = .false.
  else
    do i = 2, n - 1
      if (mod(n, i) == 0) then
        is_prime = .false.
        exit
      end if
    end do
  end if

  ! Output result
  if (is_prime) then
    print *, x
  else
    print *, y
  end if

end program main