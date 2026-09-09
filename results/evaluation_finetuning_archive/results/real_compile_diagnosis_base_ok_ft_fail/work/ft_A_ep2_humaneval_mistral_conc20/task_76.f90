program main
  implicit none
  integer :: x
  logical :: result

  ! Read input from stdin
  read(*,*) x

  ! Call the function
  result = is_simple_power(x, 2)

  ! Output the result
  print *, result
end program main