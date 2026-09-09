program x_or_y_demo
  implicit none
  integer :: n, x, y, result

  ! Hardcoded input values
  n = 7
  x = 34
  y = 12

  result = x_or_y(n, x, y)

  print *, result

contains

  function x_or_y(n, x, y) result(res)
    implicit none
    integer, intent(in) :: n, x, y
    integer :: res
    integer :: i
    logical :: is_prime

    is_prime = .true.
    if (n < 2) then
      is_prime = .false.
    else
      do i = 2, n - 1
        if (mod(n, i) == 0) then
          is_prime = .false.
          exit
        end if
      end do
    end if

    if (is_prime) then
      res = x
    else
      res = y
    end if
  end function x_or_y

end program x_or_y_demo