program main
  implicit none
  integer, parameter :: x_len = 4
  integer, dimension(x_len) :: x
  integer, dimension(:), allocatable :: result
  integer :: i

  ! Hardcoded input values
  x = [15, 33, 1422, 1]

  ! Call the function
  result = unique_digits(x_len, x)

  ! Print the result
  print *, result
end program main