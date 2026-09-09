program x_or_y_demo
  implicit none
  integer :: n, x, y, result

  ! Read input values
  read *, n
  read *, x
  read *, y

  ! Call the function
  result = x_or_y(n, x, y)

  ! Print the result
  print *, result

contains

  integer function x_or_y(n, x, y)
    implicit none
    integer, intent(in) :: n, x, y
    integer :: i

    ! Check if n is prime
    if (n <= 1) then
      x_or_y = y
    else
      x_or_y = x
      do i = 2, n - 1
        if (mod(n, i) == 0) then
          x_or_y = y
          exit
        end if
      end do
    end if
  end function x_or_y

end program x_or_y_demo