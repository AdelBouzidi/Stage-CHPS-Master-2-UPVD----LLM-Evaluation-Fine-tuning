program main
  implicit none
  integer :: x, n
  logical :: result

  read *, x
  read *, n

  result = is_simple_power(x, n)

  print *, result
end program main