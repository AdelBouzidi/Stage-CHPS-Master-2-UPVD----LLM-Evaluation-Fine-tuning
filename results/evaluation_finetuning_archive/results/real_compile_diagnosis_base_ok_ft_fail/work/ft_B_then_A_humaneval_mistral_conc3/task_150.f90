program x_or_y
  implicit none
  integer :: n, x, y
  integer :: result

  read *, n
  read *, x
  read *, y
  result = x_or_y(n, x, y)
  print *, result

contains

  integer function x_or_y(n, x, y)
    integer, intent(in) :: n, x, y
    if (prime(n)) then
      x_or_y = x
    else
      x_or_y = y
    end if
  end function x_or_y

  integer function prime(n)
    integer, intent(in) :: n
    prime = .true.
    if (n < 2) then
      prime = .false.
    else
      do i = 2, n-1
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if
  end function prime

end program x_or_y