program x_or_y
  implicit none
  integer :: n, x, y

  read *, n
  read *, x
  read *, y

  if (is_prime(n)) then
    print *, x
  else
    print *, y
  end if

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
      do i = 3, sqrt(real(n), kind=real(0))
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if
  end function is_prime

end program x_or_y