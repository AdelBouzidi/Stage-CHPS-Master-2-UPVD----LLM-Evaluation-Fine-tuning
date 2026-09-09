program main
  implicit none
  integer :: x_len
  integer, dimension(:), allocatable :: x
  integer :: i
  integer :: result_len
  integer, dimension(:), allocatable :: result

  ! Read input from stdin
  read *, x_len
  allocate(x(x_len))
  read *, x

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output the result
  print *, result
end program main