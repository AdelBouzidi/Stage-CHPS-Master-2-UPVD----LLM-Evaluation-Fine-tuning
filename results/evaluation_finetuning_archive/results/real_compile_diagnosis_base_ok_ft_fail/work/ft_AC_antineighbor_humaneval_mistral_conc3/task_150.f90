program x_or_y_demo
  implicit none
  integer :: n, x, y
  integer :: result

  ! Read input values
  read *, n
  read *, x
  read *, y

  ! Call the function
  result = x_or_y(n, x, y)

  ! Print the result
  print *, result

contains

  function x_or_y(n, x, y) result(res)
    implicit none
    integer, intent(in) :: n, x, y
    integer :: res
    integer :: i
    logical :: is_prime

    is_prime = .true.
    do i = 2, n - 1
      if (mod(n, i) == 0) then
        is_prime = .false.
        exit
      end if
    end do

    if (is_prime) then
      res = x
    else
      res = y
    end if
  end function x_or_y

end program x_or_y_demo