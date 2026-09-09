program x_or_y
  implicit none
  integer :: n, x, y, result

  ! Read input
  read(*,*) n
  read(*,*) x
  read(*,*) y

  ! Check if n is prime
  if (is_prime(n)) then
    result = x
  else
    result = y
  end if

  ! Output result
  print *, result

contains

  function is_prime(n) result(prime)
    implicit none
    integer, intent(in) :: n
    logical :: prime
    integer :: i

    if (n <= 1) then
      prime = .false.
    else if (n == 2) then
      prime = .true.
    else if (mod(n, 2) == 0) then
      prime = .false.
    else
      prime = .true.
      do while (i*i <= n)
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
        i = i + 1
      end do
    end if
  end function is_prime

end program x_or_y